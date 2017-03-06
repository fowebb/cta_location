cta_location
===============
#### Fetch CTA train location data from CTA API and store in MongoDB.

### Setup

```
> git clone git@github.com:fowebb/cta_location.git
> cd cta_location
> mkvirtualenv --no-site-packages cta_location
> workon cta_location
> add2virtualenv .
> pip install -r requirements.txt
> cp example_env.py env.py
> vim env.py    <--- add your CTA API key
```

### Get train locations for specified Route ID - will fetch/ingest locations every 60 seconds.

```
python cta_location_gatherer.py route_id
```

### Route ID Quick Reference:
- Red = Red Line (Howard-95th/Dan Ryan service)
- Blue = Blue Line (O’Hare-Forest Park service)
- Brn = Brown Line (Kimball-Loop service)
- G = Green Line (Harlem/Lake-Ashland/63rd-Cottage Grove service)
- Org = Orange Line (Midway-Loop service)
- P = Purple Line (Linden-Howard shuttle service)
- Pink = Pink Line (54th/Cermak-Loop service)
- Y = Yellow Line (Skokie-Howard [Skokie Swift] shuttle service)