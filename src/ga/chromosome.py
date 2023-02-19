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
