import pandas as pd

sheet_url = "https://azureinfogroup-my.sharepoint.com/:x:/r/personal/kundan_jadhav_data-axle_com/_layouts/15/Doc.aspx?sourcedoc=%7BD2891A1C-74D0-48D2-AF26-B8C3E4CC319E%7D&file=Order%20Tracker.xlsx&wdLOR=cEA699AB1-DEA9-4652-A4D4-62B48A3970FE&fromShare=true&action=default&mobileredirect=true"

df = pd.read_csv(sheet_url)