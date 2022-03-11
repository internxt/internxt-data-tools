import stripe
import pandas as pd


class StripeAdapter:
    def __init__(self, api_key):
        stripe.api_key = api_key
        self.stripe = stripe

    def extract_data(self, resource, start_date=None, end_date=None, **kwargs):
        if start_date:
            # convert to unix timestamp
            start_date = int(start_date.timestamp())
        if end_date:
            # convert to unix timestamp
            end_date = int(end_date.timestamp())
        resource_list = getattr(stripe, resource).list(
            limit=100, created={"gte": start_date, "lt": end_date}, **kwargs)
        lst = []
        for i in resource_list.auto_paging_iter():
            # lst.extend(list_selector(charges_schema, [i]))
            lst.extend([i])
        df = pd.DataFrame(lst)
        if len(df) > 0:
            df['created'] = pd.to_datetime(df['created'], unit='s')
        return df, lst

    def sessions(self, start_date=None, end_date=None, **kwargs):
        if start_date:
            # convert to unix timestamp
            start_date = int(start_date.timestamp())
        if end_date:
            # convert to unix timestamp
            end_date = int(end_date.timestamp())
        resource_list = self.stripe.checkout.Session.list(
            limit=100, created={"gte": start_date, "lt": end_date}, expand=['data.line_items', 'data.subscription', 'data.payment_link', 'data.payment_intent', 'data.customer'], status='complete')
        lst = []
        for i in resource_list.auto_paging_iter():
            # lst.extend(list_selector(charges_schema, [i]))
            lst.extend([i])
        df = pd.DataFrame(lst)
        if len(df) > 0:
            df['created'] = pd.to_datetime(df['created'], unit='s')
        return df, lst
