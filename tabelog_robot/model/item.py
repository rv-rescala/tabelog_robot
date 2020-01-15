from dataclasses import dataclass, field

@dataclass(frozen=True)
class Item:
    id: str
    name: str
    url: str
    img_src: str
    category: str

@dataclass(frozen=True)
class RankedItem:
    item_id: str
    ranking_url: str
    item_name: str
    item_img_src: str
    item_maker: str
    item_category: str
    item_rank: int
    rank_category: str
    rank_gathered_date: str
    item_url: str
    item_min_price: str
    item_review_rate: str
    item_bbs_num: str