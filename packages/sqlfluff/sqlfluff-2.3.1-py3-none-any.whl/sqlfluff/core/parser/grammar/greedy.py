"""GreedyUntil and StartsWith Grammars."""

from typing import List, Optional, Tuple, Union

from sqlfluff.core.parser.context import ParseContext
from sqlfluff.core.parser.grammar.base import (
    BaseGrammar,
    BaseSegment,
    cached_method_for_parse_context,
)
from sqlfluff.core.parser.helpers import trim_non_code_segments
from sqlfluff.core.parser.match_result import MatchResult
from sqlfluff.core.parser.match_wrapper import match_wrapper
from sqlfluff.core.parser.segments import allow_ephemeral
from sqlfluff.core.parser.types import MatchableType, SimpleHintType


class GreedyUntil(BaseGrammar):
    """Matching for GreedyUntil works just how you'd expect.

    Args:
        enforce_whitespace_preceding (:obj:`bool`): Should the GreedyUntil
            match only match the content if it's preceded by whitespace?
            (defaults to False). This is useful for some keywords which may
            have false alarms on some array accessors.

    """

    def __init__(
        self,
        *args: Union[MatchableType, str],
        enforce_whitespace_preceding_terminator: bool = False,
        optional: bool = False,
        ephemeral_name: Optional[str] = None,
    ) -> None:
        self.enforce_whitespace_preceding_terminator = (
            enforce_whitespace_preceding_terminator
        )
        # NOTE: This grammar does not support allow_gaps=False,
        # therefore that option is not provided here.
        super().__init__(*args, optional=optional, ephemeral_name=ephemeral_name)

    @match_wrapper()
    @allow_ephemeral
    def match(
        self, segments: Tuple[BaseSegment, ...], parse_context: ParseContext
    ) -> MatchResult:
        """Matching for GreedyUntil works just how you'd expect."""
        return self.greedy_match(
            segments,
            parse_context,
            matchers=self._elements,
            enforce_whitespace_preceding_terminator=(
                self.enforce_whitespace_preceding_terminator
            ),
            include_terminator=False,
        )

    @classmethod
    def greedy_match(
        cls,
        segments: Tuple[BaseSegment, ...],
        parse_context: ParseContext,
        matchers: List[MatchableType],
        enforce_whitespace_preceding_terminator: bool,
        include_terminator: bool = False,
    ) -> MatchResult:
        """Matching for GreedyUntil works just how you'd expect."""
        seg_buff = segments
        seg_bank: Tuple[BaseSegment, ...] = ()  # Empty tuple

        while True:
            with parse_context.deeper_match(name="GreedyUntil") as ctx:
                pre, mat, _ = cls._bracket_sensitive_look_ahead_match(
                    seg_buff, matchers, parse_context=ctx
                )

            # Do we have a match?
            if mat:
                # Do we need to enforce whitespace preceding?
                if enforce_whitespace_preceding_terminator:
                    # Does the match include some whitespace already?
                    # Work forward
                    idx = 0
                    while True:
                        elem = mat.matched_segments[idx]
                        if elem.is_meta:  # pragma: no cover TODO?
                            idx += 1
                            continue
                        elif elem.is_type(
                            "whitespace", "newline"
                        ):  # pragma: no cover TODO?
                            allowable_match = True
                            break
                        else:
                            # No whitespace before. Not allowed.
                            allowable_match = False
                            break

                    # If we're not ok yet, work backward to the preceding sections.
                    if not allowable_match:
                        idx = -1
                        while True:
                            if len(pre) < abs(idx):  # pragma: no cover TODO?
                                # If we're at the start, it's ok
                                allowable_match = True
                                break
                            if pre[idx].is_meta:  # pragma: no cover TODO?
                                idx -= 1
                                continue
                            elif pre[idx].is_type("whitespace", "newline"):
                                allowable_match = True
                                break
                            else:
                                # No whitespace before. Not allowed.
                                allowable_match = False
                                break

                    # If this match isn't preceded by whitespace and that is
                    # a requirement, then we can't use it. Carry on...
                    if not allowable_match:
                        # Update our buffers and continue onward
                        seg_bank = seg_bank + pre + mat.matched_segments
                        seg_buff = mat.unmatched_segments
                        # Loop around, don't return yet
                        continue

                # Depending on whether we found a terminator or not we treat
                # the result slightly differently. If no terminator was found,
                # we just use the whole unmatched segment. If we did find one,
                # we match up until (but not including [unless self.include_terminator
                # is true]) that terminator.
                if mat:
                    # Return everything up to the match unless it's a gap matcher.
                    if include_terminator:
                        return MatchResult(
                            seg_bank + pre + mat.matched_segments,
                            mat.unmatched_segments,
                        )

                    # We can't claim any non-code segments, so we trim them off the end.
                    leading_nc, pre_seg_mid, trailing_nc = trim_non_code_segments(
                        seg_bank + pre
                    )
                    return MatchResult(
                        leading_nc + pre_seg_mid,
                        trailing_nc + mat.all_segments(),
                    )
                # No terminator, just return the whole thing.
                return MatchResult.from_matched(
                    mat.unmatched_segments
                )  # pragma: no cover TODO?
            else:
                # Return everything
                return MatchResult.from_matched(segments)


class StartsWith(GreedyUntil):
    """Match if this sequence starts with a match.

    This also has configurable whitespace and comment handling.
    """

    def __init__(
        self,
        target: Union[MatchableType, str],
        *args: Union[MatchableType, str],
        # NOTE: Other grammars support terminators (plural)
        # TODO: Align these to be the same eventually.
        terminator: Optional[Union[MatchableType, str]] = None,
        include_terminator: bool = False,
        enforce_whitespace_preceding_terminator: bool = False,
        optional: bool = False,
        ephemeral_name: Optional[str] = None,
    ) -> None:
        self.target = self._resolve_ref(target)
        self.terminator = self._resolve_ref(terminator)
        self.include_terminator = include_terminator

        # StartsWith should only be used with a terminator
        assert self.terminator

        super().__init__(
            *args,
            enforce_whitespace_preceding_terminator=enforce_whitespace_preceding_terminator,  # noqa: E501
            optional=optional,
            ephemeral_name=ephemeral_name,
        )

    @cached_method_for_parse_context
    def simple(
        self, parse_context: ParseContext, crumbs: Optional[Tuple[str]] = None
    ) -> SimpleHintType:
        """Does this matcher support a uppercase hash matching route?

        `StartsWith` is simple, if the thing it starts with is also simple.
        """
        return self.target.simple(parse_context=parse_context, crumbs=crumbs)

    @match_wrapper()
    def match(
        self, segments: Tuple[BaseSegment, ...], parse_context: ParseContext
    ) -> MatchResult:
        """Match if this sequence starts with a match."""
        first_code_idx = None
        # Work through to find the first code segment...
        for idx, seg in enumerate(segments):
            if seg.is_code:
                first_code_idx = idx
                break
        else:
            # We've trying to match on a sequence of segments which contain no code.
            # That means this isn't a match.
            return MatchResult.from_unmatched(segments)  # pragma: no cover TODO?
        with parse_context.deeper_match(name="StartsWith") as ctx:
            match = self.target.match(segments[first_code_idx:], ctx)

        if not match:
            return MatchResult.from_unmatched(segments)

        # The match will probably have returned a mutated version rather
        # that the raw segment sent for matching. We need to reinsert it
        # back into the sequence in place of the raw one, but we can't
        # just assign at the index because it's a tuple and not a list.
        # to get around that we do this slightly more elaborate construction.

        # NB: This match may be partial or full, either is cool. In the case
        # of a partial match, given that we're only interested in what it STARTS
        # with, then we can still used the unmatched parts on the end.
        # We still need to deal with any non-code segments at the start.
        assert self.terminator
        greedy_match = self.greedy_match(
            match.unmatched_segments,
            parse_context,
            matchers=[self.terminator],
            enforce_whitespace_preceding_terminator=(
                self.enforce_whitespace_preceding_terminator
            ),
            include_terminator=self.include_terminator,
        )

        # NB: If all we matched in the greedy match was non-code then we can't
        # claim it.
        if not any(seg.is_code for seg in greedy_match.matched_segments):
            # So just return the original match.
            return match

        # Otherwise Combine the results.
        return MatchResult(
            match.matched_segments + greedy_match.matched_segments,
            greedy_match.unmatched_segments,
        )
