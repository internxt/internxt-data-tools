import stripe
import pandas as pd
from . import utils


class StripeAdapter:
    def __init__(self, api_key):
        stripe.api_key = api_key
        self.stripe = stripe

    def __extract_data(self, resource, start_date=None, end_date=None, **kwargs):
        if start_date:
            # convert to unix timestamp
            start_date = int(start_date.timestamp())
        if end_date:
            # convert to unix timestamp
            end_date = int(end_date.timestamp())
        resource_list = getattr(self.stripe, resource).list(
            limit=100, created={"gte": start_date, "lt": end_date}, **kwargs)
        lst = []
        for i in resource_list.auto_paging_iter():
            lst.extend([i])
        df = pd.DataFrame(lst)
        if len(df) > 0:
            df['created'] = pd.to_datetime(df['created'], unit='s')
        return df, lst

    def extract(self, item, init, end, schema, **kwargs):
      if(item == 'Session'):
        df_c, items_list = self.stripe.sessions(start_date=init,
                                             end_date=end)
      else:
        df_c, items_list = self.__extract_data(item, start_date=init,
                                               end_date=end, **kwargs)
      without_lists = utils.bulk_remove_lists(items_list)
      f = utils.extract_schema_data(schema, without_lists)
      return pd.DataFrame(f)
