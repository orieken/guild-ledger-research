# P2 — detailed

Add a complete quest-acceptance flow to the existing Guild Ledger application. The player selects a quest, an existing party, and equipment quantities, then submits the expedition from the Vue UI. Reserve the equipment through the Go armory service, save its reservation ID on the accepted expedition in Python, and display the persisted result after a reload.

A quest must be open. The party's size must fall within the quest's inclusive minimum and maximum, and every member must meet the quest's minimum character level. A party already assigned to a pending or accepted expedition cannot accept another one.

Request equipment as one atomic reservation. If any requested equipment is unavailable, show a useful failure, create no accepted expedition, and leave no active reservation for that failed request.

While submitting, show a pending state and prevent repeated clicks from submitting another request. Keep the selected party and equipment values after a failed submission so the player can correct the request or retry.

Preserve existing quest browsing and party selection. Add appropriate tests, run the available checks, and record the results and any assumptions.
