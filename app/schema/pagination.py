from pydantic import BaseModel


class PaginationRequest(BaseModel):
    page: int = 1
    size: int = 1

    @property
    def offset(self):
        return self.size * (self.page - 1)


def get_pagination_response(result_type: any):
    class PaginationResponse(BaseModel):
        total: int
        next_page: int = None
        prev_page: int = None
        results: result_type

    return PaginationResponse
