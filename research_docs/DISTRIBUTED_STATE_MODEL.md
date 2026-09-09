# EdgeSync Research Dossier: Formal Distributed State & Gossip Model

**Target Conference:** IEEE PerCom 2027  
**Document ID:** `DISTRIBUTED_STATE_MODEL.md`

---

## 1. Mathematical Formalization of Regional Node State

Let $\mathcal{N} = \{N_{\text{EAST}}, N_{\text{WEST}}, N_{\text{CENTRAL}}\}$ be the set of regional edge nodes in the EdgeSync cluster.

Each node $N_i \in \mathcal{N}$ maintains a bounded observation reservoir $\mathcal{S}_i \subset \mathcal{O}$, where $\mathcal{O}$ is the universe of unique food delivery ETA observations generated across the city.

### Definition 1.1 (Observation Tuple)
An ETA observation $o \in \mathcal{O}$ is a 4-tuple:

$$o = \langle \text{id}, t, r, y \rangle$$

where:
- $\text{id} \in \mathbb{U}$ is a universally unique identifier (UUID v4),
- $t \in \mathbb{R}^+$ is the Unix epoch timestamp (seconds) when the order request was processed,
- $r \in \{\text{EAST}, \text{WEST}, \text{CENTRAL}\}$ is the origin edge region,
- $y \in \mathbb{R}^+$ is the computed total ETA value (minutes).

---

## 2. Distributed State Merging & Set Union Mechanics

When node $N_i$ receives a gossip synchronization payload containing observation set $\mathcal{S}_{\text{incoming}}$ from peer node $N_j$, the state update operator $\oplus$ is defined as:

$$\mathcal{S}_i^{(t+1)} = \mathcal{S}_i^{(t)} \oplus \mathcal{S}_{\text{incoming}} = \mathcal{S}_i^{(t)} \cup \mathcal{S}_{\text{incoming}}$$

The aggregated fleet-wide average ETA $A_i$ computed at node $N_i$ is given by:

$$A_i = \begin{cases} 
0, & \text{if } |\mathcal{S}_i| = 0 \\ 
\frac{1}{|\mathcal{S}_i|} \sum_{o \in \mathcal{S}_i} o.y, & \text{if } |\mathcal{S}_i| > 0 
\end{cases}$$

The total valid sample count reported by $N_i$ is simply $n_i = |\mathcal{S}_i|$.

---

## 3. Algebraic Properties & Distributed System Guarantees

### Theorem 3.1 (Idempotence)
*For any observation state $\mathcal{S}$, the merge operation satisfies $\mathcal{S} \oplus \mathcal{S} = \mathcal{S}$.*

**Proof:**  
By definition, $\mathcal{S} \oplus \mathcal{S} = \mathcal{S} \cup \mathcal{S}$. In standard set theory, set union is idempotent: $\forall x (x \in \mathcal{S} \cup \mathcal{S} \iff x \in \mathcal{S})$. Thus, receiving duplicate gossip messages, retrying network calls, or receiving messages that have circulated around a ring loop ($N_{\text{EAST}} \rightarrow N_{\text{WEST}} \rightarrow N_{\text{CENTRAL}} \rightarrow N_{\text{EAST}}$) introduces zero duplicate observations into $\mathcal{S}_i$. $\blacksquare$

---

### Theorem 3.2 (Commutativity)
*For any two observation states $\mathcal{A}$ and $\mathcal{B}$, $\mathcal{A} \oplus \mathcal{B} = \mathcal{B} \oplus \mathcal{A}$.*

**Proof:**  
$\mathcal{A} \cup \mathcal{B} = \mathcal{B} \cup \mathcal{A}$. The physical arrival order of gossip packets across network interfaces does not impact the merged state. $\blacksquare$

---

### Theorem 3.3 (Associativity)
*For any three observation states $\mathcal{A}, \mathcal{B}, \mathcal{C}$, $(\mathcal{A} \oplus \mathcal{B}) \oplus \mathcal{C} = \mathcal{A} \oplus (\mathcal{B} \oplus \mathcal{C})$.*

**Proof:**  
Set union is associative: $(\mathcal{A} \cup \mathcal{B}) \cup \mathcal{C} = \mathcal{A} \cup (\mathcal{B} \cup \mathcal{C})$. Intermediate network routing hops do not alter the final converged state. $\blacksquare$

---

## 4. Operational Failure Scenarios & State Recovery

1. **Duplicate Messages:** Filtered out automatically by set key matching ($\text{obs\_id}$).
2. **Looping Gossip Ring Messages:** Messages cycling through the ring topology contain known observation IDs; set size $|\mathcal{S}|$ remains invariant.
3. **Stale / Outdated Observations:** Observations older than a configurable sliding window $W_{\text{window}}$ (e.g. $t < t_{\text{now}} - 600\text{s}$) are pruned during interval maintenance.
4. **Node Restart Recovery:** A node restarting with $\mathcal{S}_i = \emptyset$ absorbs the complete global observation set $\mathcal{S}_{\text{peer}}$ upon receiving its first gossip `/sync` payload.
