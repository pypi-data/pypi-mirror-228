from bewe.alpha_seeker import base_data
from bewe.services.databases import asset_orm
from bewe.services.databases import db_manager
import pandas as pd
import numpy as np
import tensorflow as tf


class DailyStock(base_data.DataContainer):

    def __init__(self):
        super().__init__(asset_name='daily_stock')
        self.db = db_manager.DBManager()
        self.format = base_data.DataFormat(
            required_field=['feature', 'label']
        )

    def query_stock(self, stock_id, limit=100):
        records = self.db.query(
            asset_orm.StockPrice,
            conditions={'stock_id': stock_id},
            order_conditions={'date': False},
            limit=limit
        )
        records = [r.get_dict() for r in records]
        df = pd.DataFrame(records).sort_values('date')
        return df

    def get_level(self, value):
        return min(int(value*100) + 10, 10)

    def transform(self, data: pd.DataFrame):
        self.data = []

        data['actionable_price'] = data['open_price'].shift(-1)
        data['val_start'] = data['close_price'].shift(-1)
        data['val_end'] = data['close_price'].shift(-6)
        data = data[~data['val_end'].isna()]
        data['daily_diff'] = data.apply(
            lambda row: self.get_level(
                (row.close_price-row.open_price)/row.open_price
            ),
            axis=1
        )
        data['label'] = data.apply(
            lambda row: self.get_level(
                (row.val_end-row.val_start)/row.val_start
            ),
            axis=1
        )

        data['feat'] = [window.to_list() for window in data.daily_diff.rolling(window=10)]
        data['quality'] = [len(r) >= 10 for r in data.feat.values]
        data = data[data['quality']]

        for _, row in data.iterrows():
            row = base_data.DataUnit(
                format=self.format,
                data={
                    'feature': row.feat,
                    'label': row.label
                },
                actionable_price=row['actionable_price']
            )
            self.data.append(row)
        self.size = len(self.data)


if __name__ == '__main__':

    features = []
    labels = []

    for stock in ['2330', '4919', '0050', '0056', '2356', '3231']:
        loader = DailyStock()
        loader_data = loader.query_stock(stock, limit=200)
        loader.transform(loader_data)

        for row in loader:
            features.append(row.data['feature'])
            labels.append(row.data['label'])

    features = np.array(features)
    labels = np.array(labels)
    shuffle_index = np.arange(len(labels))
    np.random.shuffle(shuffle_index)

    features = features[shuffle_index]
    labels = labels[shuffle_index]

    import collections
    print(collections.Counter(labels))

    tf.keras.backend.clear_session()
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Embedding(20, 32))
    model.add(tf.keras.layers.LSTM(32))
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(20, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['acc'])

    model.fit(features, labels, epochs=10, validation_split=0.1)
