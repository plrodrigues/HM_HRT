from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class Chromosome:
    mode: list[str]
    order: list[int]

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(
            {
                "task_id": [x for x in range(len(self.mode))],
                "mode": self.mode,
                "order": self.order,
            },
        )
        df = df.set_index("task_id")
        return df

    def is_equal(self, chromosome_to_compare) -> bool:
        return (self.mode == chromosome_to_compare.mode) and (
            self.order == chromosome_to_compare.order
        )
