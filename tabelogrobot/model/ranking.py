from dataclasses import dataclass, field

@dataclass(frozen=True)
class RankedItem:
    shop_name: str
    shop_link: str
    shop_target: str
    shop_photo: str
    shop_start: str
    shop_review_count: str
    shop_review_link: str
    shop_diner_budget: str
    shop_lunch_budget: str
    shop_comments: str
    shop_pr_comment_title: str
    shop_pr_comment_first: str