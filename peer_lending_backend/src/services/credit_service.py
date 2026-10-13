from peer_lending_backend.src.schemas.credit import (
    CreditScoreRequest,
    CreditScoreResponse,
)


class CreditService:
    """Provides a demo-only heuristic; scores are not persisted."""

    def __init__(self):
        self._scores: dict[int, CreditScoreResponse] = {}

    def score(self, payload: CreditScoreRequest) -> CreditScoreResponse:
        debt_ratio = payload.existing_debt / payload.income
        score = 300 + (5 * payload.payment_history_score) - min(
            200, debt_ratio * 100
        )
        result = CreditScoreResponse(
            borrower_id=payload.borrower_id,
            score=round(max(300, min(850, score)), 2),
        )
        self._scores[payload.borrower_id] = result
        return result

    def retrieve(self, borrower_id: int) -> CreditScoreResponse | None:
        return self._scores.get(borrower_id)
