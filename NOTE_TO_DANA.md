Hi Dana,

After checking the data, I found two main issues.

1. The check-in data from **Jul 13–16, 2026** is missing. After checking with your manager, I confirmed that arrivals were not recorded during these four weekdays because the check-in system was down. These days are excluded from desk usage and booked-but-unused calculations.
2. For about **20% of the records**, the check-in time is earlier than the booking time. In practice, this may mean that people arrived at a desk first and only created the booking afterward. In this dashboard, I assume these records are cases like this. This assumption may be wrong if the timestamp difference was actually caused by a system issue.

**Apart from Jul 13–16, 2026, I assume that the rest of the data is accurate and reliable enough for this analysis.** I checked for duplicate bookings, desks being booked twice on the same day, employees booking more than one desk on the same day, and employees appearing under different teams, and did not find any of these issues. The booking dates are complete, and every recorded check-in happened on the correct booking day.

In this dashboard, a **used desk** means a booking where the person checked in, regardless of when the booking was created. You can hover over the charts for more detail and click them to drill down into the underlying bookings.

For the questions you care about:

1. **How full is each floor?** (By floor and by day of the week.)

The four floors are used at very similar levels, averaging about 46–48% desk usage. Across the office, about **47%** of desks are **actually used** on an average reliable check-in day, while about **30%** are **booked but unused**. The bigger difference is by weekday: Tuesday and Wednesday are the busiest at 65% and 67% usage, while Friday is much quieter at 18%.

You can see this in the first section of the dashboard, which breaks down actually used, booked but unused, and not booked desks by floor and weekday.

2. **How much space is booked and never used?** (How many desk-days go to no-shows, and whether it's concentrated anywhere)
  
There are 4,984 booked-but-unused desk-days in total. Unused bookings are concentrated more by **weekday and team than by floor**. Fridays are worst (42% of bookings unused) and Tuesdays best (27%). Data leaves 46% of its bookings unused, People only 17%. The largest concentration come from Engineering Team on Tuesdays, with 342 unused desk-days, meaning 40% of Engineering’s Tuesday bookings were unused. In contrast, all four floors have similar unused-booking rates of around 30%. 

You can see these patterns in the team-by-weekday heatmap in the dashboard.

3. **Can we give back a floor?**

The answer depends on whether we look at **actual attendance or booking demand**. The dashboard compares the data with 310 desks, which is the assumed capacity of three floors.

On **0 of 62 reliable days** did more than **310 people actually check in**, which suggests that three floors could accommodate the people who actually came to the office. However, on **26 of 66 office days**, more than **310 desks were booked**. On those days, an average of 361 desks were booked — **51 more than three-floor capacity** - and these days were concentrated mainly on Tuesdays and Wednesdays.  

Based on this, it is still too early to conclude whether we should give back a floor based on this data alone. Actual usage suggests three floors may be enough, but the current booking pattern suggests otherwise. Before making the lease decision, I would look at a longer period of data and test whether reducing no-shows or changing the booking policy could bring booking demand below 310 more consistently.

Hope the dashboard is helpful and feel free to let me know any concerns. Thank you!

Best, 
Lucy (Yalu Pan)
