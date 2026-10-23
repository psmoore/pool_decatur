# City of Decatur Aquatics — unofficial preview

A mock-up of [Decatur's Aquatics pages](https://www.decaturga.com/parksrec/page/aquatics) (Aquatics, Aquatics Programs, and a
page per pool: Oakhurst, Ebster, Glenlake, McKoy) with all four pools on live [Pool Relay](https://www.poolrelay.com)
schedules. Not operated by or affiliated with the City of Decatur or Dynamo Swim School.

No schedule is typed into the pages. The "where can I swim now" board, each pool's right-now card, hours, holiday closures,
the week table and every Dynamo class's days and times are filled by `finder.js` from the live views; `build.py` holds only
fees, passes, policies and facts about the water.

- `build.py`: generates the six pages. `V` holds the four Pool Relay share tokens (one view per pool).
- `finder.js`: `#finder` (board), `#today`, `#week` (by kind of session for one pool), and `data-live`
  (`hours`, `when`, `exceptions`, `swims`, `closures`).
