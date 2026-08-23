# EdgeSync Research Dossier: ETA Model Deep Analysis

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `03_ETA_MODEL_DEEP_ANALYSIS.md`

---

## 1. Mathematical & Algorithmic Formulation

The ETA model in EdgeSync computes total delivery time based on three modular components:
1. **Rider Pickup Time ($T_{\text{pickup}}$):** Time required for a delivery rider to reach the restaurant.
2. **Food Preparation Time ($T_{\text{prep}}$):** Time required for the restaurant to cook and package the order.
3. **Delivery Travel Time ($T_{\text{delivery}}$):** Time required to travel from the restaurant to the customer destination.

The total ETA equation implemented across all microservices is:

$$\text{ETA} = \max(T_{\text{pickup}}, T_{\text{prep}}) + T_{\text{delivery}}$$

```text
File: east.py / west.py / central.py
function/class: custom_eta()
line number: Line 60
relevant behavior: ETA = max(pickup, prep) + delivery
```

---

## 2. Component Analysis

### A. Distance Calculation (Haversine Formula)

Great-circle distance between two geographic coordinates $P_1 = (\text{lat}_1, \text{lon}_1)$ and $P_2 = (\text{lat}_2, \text{lon}_2)$ is computed in kilometers using the Earth radius $R = 6371\text{ km}$:

$$\Delta \text{lat} = \text{radians}(\text{lat}_2 - \text{lat}_1), \quad \Delta \text{lon} = \text{radians}(\text{lon}_2 - \text{lon}_1)$$
$$a = \sin^2\left(\frac{\Delta \text{lat}}{2}\right) + \cos(\text{radians}(\text{lat}_1)) \cdot \cos(\text{radians}(\text{lat}_2)) \cdot \sin^2\left(\frac{\Delta \text{lon}}{2}\right)$$
$$c = 2 \cdot \text{atan2}(\sqrt{a}, \sqrt{1 - a})$$
$$d = R \cdot c$$

```text
File: utils.py
function/class: distance(p1, p2)
line range: Lines 6-17
purpose: Calculates Haversine distance in km.
```

---

### B. Traffic & Speed Model

Travel time for a given distance $d$ (in km) and traffic level $\text{Traffic} \in \{\text{"Low"}, \text{"Medium"}, \text{"High"}\}$ is:

$$T_{\text{delivery}} = \left(\frac{d}{\text{Speed}(\text{Traffic})}\right) \times 60 \text{ minutes}$$

#### Speed Mapping:
- **Low Traffic:** $35\text{ km/h}$
- **Medium Traffic:** $25\text{ km/h}$
- **High Traffic:** $15\text{ km/h}$

```text
File: utils.py
function/class: estimate_time_from_distance(distance_km, traffic_level)
line range: Lines 20-28
```

#### Dynamic Time-of-Day Selection (`dynamic_traffic()`):
If `traffic` parameter is not explicitly passed by the caller, traffic level is resolved based on local system hour (`datetime.now().hour`):
- Hours $8 \le h \le 11$ OR $17 \le h \le 21$: **"High"**
- Hours $12 \le h \le 16$: **"Medium"**
- All other hours: **"Low"**

```text
File: utils.py
function/class: dynamic_traffic()
line range: Lines 31-39
```

---

### C. Rider Proximity Model

Rider pickup time is computed from user-selected proximity options:

$$\text{RiderDistance}_{\text{mean}} = \frac{\text{LowRange} + \text{HighRange}}{2}$$
$$\text{RiderDistance} = \text{RiderDistance}_{\text{mean}} \times \text{Uniform}(0.9, 1.1)$$
$$T_{\text{pickup}} = \text{RiderDistance} \times 2$$

*(Note: The factor of 2 models a fixed 30 km/h average rider travel speed to the restaurant: $\frac{d}{30} \times 60 = 2d$.)*

#### Proximity Buckets:
- **"Near (0.5-2 km)":** Range $[0.5, 2.0]\text{ km}$, Mean $= 1.25\text{ km}$
- **"Medium (2-5 km)":** Range $[2.0, 5.0]\text{ km}$, Mean $= 3.5\text{ km}$
- **"Far (5-8 km)":** Range $[5.0, 8.0]\text{ km}$, Mean $= 6.5\text{ km}$

```text
File: utils.py & east.py
function/class: get_rider_distance_from_option(option) (utils.py:L42-L50), custom_eta() (east.py:L30)
```

---

### D. Food Preparation Model & Implementation Bug Analysis

Preparation time is parameterized by food category:

$$T_{\text{prep}} = \left(\frac{\text{Prep}_{\text{low}} + \text{Prep}_{\text{high}}}{2}\right) \times \text{Uniform}(0.9, 1.1)$$

#### Preparation Time Ranges:
- `"pizza"`: $[12, 18]\text{ min}$, Mean $= 15.0\text{ min}$
- `"burger"`: $[8, 12]\text{ min}$, Mean $= 10.0\text{ min}$
- `"sandwich"`: $[5, 8]\text{ min}$, Mean $= 6.5\text{ min}$
- `"taco"`: $[6, 10]\text{ min}$, Mean $= 8.0\text{ min}$
- **Default Fallback:** $[5, 10]\text{ min}$, Mean $= 7.5\text{ min}$

```text
File: utils.py
function/class: get_prep_time(food)
line range: Lines 53-62
```

> [!CAUTION]
> **CRITICAL CODE BUG DISCOVERED:**  
> In `ui.py:L90`, the Streamlit frontend dropdown passes capitalized food names: `["Pizza", "Burger", "Sandwich", "Taco"]`.  
> However, in `utils.py:L54-L59`, the `prep_times` dictionary uses **lowercase keys**: `"pizza"`, `"burger"`, `"sandwich"`, `"taco"`.  
> Because Python dictionary lookups are case-sensitive (`prep_times.get(food, (5, 10))`), passing `"Pizza"` fails the key check and **ALWAYS returns the fallback default range `(5, 10)` (mean 7.5 mins)** regardless of user food selection!

---

## 3. Step-by-Step Numerical Examples

### Example 1: Intra-Region Order (Powai to Powai, High Traffic)
- **Parameters:** Source `[19.1197, 72.9050]` (EAST), Destination `[19.1300, 72.9150]` (EAST), Food `"burger"`, Rider `"Near (0.5-2 km)"`, Traffic `"High"`.
- **Haversine Distance:** $1.56\text{ km}$
- **Pickup Time:** $1.25 \times 1.00 \times 2 = 2.50\text{ mins}$
- **Prep Time:** $10.0 \times 1.00 = 10.00\text{ mins}$
- **Delivery Time:** $(1.56 / 15) \times 60 = 6.24\text{ mins}$
- **Calculated ETA:** $\max(2.50, 10.00) + 6.24 = 16.24\text{ mins}$

### Example 2: Cross-Region Order (Powai [EAST] to Bandra [WEST], High Traffic)
- **Parameters:** Source `[19.1197, 72.9050]` (EAST), Destination `[19.0596, 72.8295]` (WEST), Food `"pizza"`, Rider `"Far (5-8 km)"`, Traffic `"High"`.
- **Haversine Distance:** $10.32\text{ km}$
- **Pickup Time:** $6.50 \times 1.00 \times 2 = 13.00\text{ mins}$
- **Prep Time:** $15.0 \times 1.00 = 15.00\text{ mins}$
- **Delivery Time (via `http://localhost:9000/calc_delivery`):** $(10.32 / 15) \times 60 = 41.28\text{ mins}$
- **Calculated ETA:** $\max(13.00, 15.00) + 41.28 = 56.28\text{ mins}$

---

## 4. Discrepancies: Code vs Paper Claims

| Paper Claim | Code Implementation | Status |
| :--- | :--- | :--- |
| "Machine learning models like LightGBM for ETA" | Purely heuristic formula using speed constants (15, 25, 35 km/h) | **NOT IMPLEMENTED** |
| "Dynamic traffic from real-time feeds (Google/HERE)" | Discrete time-of-day clock check in `utils.py:L31-L39` | **NOT IMPLEMENTED** |
| "Continuous stochastic modeling of rider availability" | Pseudo-random uniform noise multiplier `random.uniform(0.9, 1.1)` | **IMPLEMENTED BUT NOT QUANTITATIVELY EVALUATED** |
| "Reproducible scientific evaluation" | No random seed initialization (`random.seed()`) in code | **NOT IMPLEMENTED** |
