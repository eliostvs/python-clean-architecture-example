import string
from decimal import getcontext

import hypothesis.strategies as st

from example.core.entities.geo import Point

getcontext().prec = 7

latitude_st = st.decimals(min_value=-90, max_value=90, allow_infinity=False, places=7)
longitude_st = st.decimals(
    min_value=-180, max_value=180, allow_infinity=False, places=7
)
point_st = st.builds(Point, latitude=latitude_st, longitude=longitude_st)
user_id_st = st.integers(min_value=0)
customer_name_st = st.text(min_size=1, alphabet=string.ascii_letters)
