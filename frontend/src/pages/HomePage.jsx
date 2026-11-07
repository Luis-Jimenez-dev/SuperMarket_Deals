import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function HomePage() {
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)

  const [postalCode, setPostalCode] = useState(() => {
    return localStorage.getItem("postalCode") ?? ""
  })

  const [nearbyStores, setNearbyStores] = useState([])

  const [selectedStore, setSelectedStore] = useState(() => {
    const savedStore = localStorage.getItem("selectedStore")

    return savedStore
      ? JSON.parse(savedStore)
      : null
  })

  // If a saved store exists, deals will load when the page first opens
  const [dealsLoading, setDealsLoading] = useState(
    () => selectedStore !== null
  )

  const [mealPlanLoading, setMealPlanLoading] = useState(false)

  // Error states
  const [storeSearchError, setStoreSearchError] = useState("")
  const [dealsError, setDealsError] = useState("")
  const [mealPlanError, setMealPlanError] = useState("")

  const navigate = useNavigate()

  // Find nearby stores using the ZIP code
  const findNearbyStores = async () => {
    setStoreSearchError("")
    setNearbyStores([])

    try {
      const response = await fetch(
        `http://localhost:8000/stores/nearby?postal_code=${postalCode}`
      )

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail)
      }

      const data = await response.json()

      setNearbyStores(data)
      localStorage.setItem("postalCode", postalCode)

    } catch (error) {
      console.error("Failed to find nearby stores:", error)
      setStoreSearchError(error.message)
    }
  }

  // Save the selected store and prepare to load its deals
  const selectStore = (store) => {
    setDealsLoading(true)
    setDeals([])
    setDealsError("")
    setMealPlanError("")
    setSelectedStore(store)

    localStorage.setItem(
      "selectedStore",
      JSON.stringify(store)
    )
  }

  // Clear the current store and show nearby stores again
  const changeStore = () => {
    setSelectedStore(null)
    setDeals([])
    setDealsLoading(false)
    setDealsError("")
    setMealPlanError("")

    localStorage.removeItem("selectedStore")

    if (postalCode) {
      findNearbyStores()
    }
  }

  // Load deals whenever the selected store changes
  useEffect(() => {
    if (!selectedStore) {
      return
    }

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/deals`
    )
      .then(async response => {
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail)
        }

        return response.json()
      })
      .then(data => {
        setDeals(data)
      })
      .catch(error => {
        console.error("Failed to load deals:", error)
        setDealsError(error.message)
      })
      .finally(() => {
        setDealsLoading(false)
      })

  }, [selectedStore])

  // Generate a meal plan using the currently selected store
  function generateMealPlan() {
    if (
      !selectedStore ||
      meals < 1 ||
      meals > 14 ||
      dealsLoading ||
      deals.length === 0
    ) {
      return
    }

    setMealPlanError("")
    setMealPlanLoading(true)

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore.store_id}/meal-plan?meals=${meals}`
    )
      .then(async response => {
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail)
        }

        return response.json()
      })
      .then(data => {
        navigate('/meal-plan', {
          state: {
            mealPlan: data,
            store: selectedStore
          }
        })
      })
      .catch(error => {
        console.error("Failed to generate meal plan:", error)
        setMealPlanError(error.message)
      })
      .finally(() => {
        setMealPlanLoading(false)
      })
  }

  return (
    <div className="app">

      {selectedStore ? (
        <section className="store-info">
          <p>Shopping at:</p>

          <h2>{selectedStore.name}</h2>

          <p>
            {selectedStore.city}, {selectedStore.state}
          </p>

          {dealsLoading ? (
            <p>Loading this week's deals...</p>
          ) : dealsError ? (
            <p>Deals unavailable</p>
          ) : (
            <p>
              {deals.length === 1
                ? "1 deal found"
                : `${deals.length} deals found`}
            </p>
          )}

          <button
            onClick={changeStore}
            disabled={dealsLoading}
          >
            Change Store
          </button>
        </section>

      ) : (
        <section className="store-search">
          <p>Find a store near you</p>

          <input
            type="text"
            value={postalCode}
            maxLength={5}
            placeholder="ZIP code"
            onChange={(event) =>
              setPostalCode(event.target.value)
            }
          />

          <button onClick={findNearbyStores}>
            Find Stores
          </button>

          {storeSearchError && (
            <p className="error-message">
              {storeSearchError}
            </p>
          )}

          {nearbyStores.length > 0 && (
            <select
              defaultValue=""
              onChange={(event) => {
                const store = nearbyStores.find(
                  (store) =>
                    store.store_id === Number(event.target.value)
                )

                if (store) {
                  selectStore(store)
                }
              }}
            >
              <option value="" disabled>
                Choose a store
              </option>

              {nearbyStores.map((store) => (
                <option
                  key={store.store_id}
                  value={store.store_id}
                >
                  {store.name} — {store.distance} miles
                </option>
              ))}
            </select>
          )}
        </section>
      )}

      <section className="weekly-deals-preview">

        <div className="section-header">
          <h2>Weekly Deals</h2>

          {selectedStore &&
            !dealsLoading &&
            !dealsError && (
              <Link to="/deals">
                View All Deals
              </Link>
            )}
        </div>

        {!selectedStore ? (
          <p>
            Select a store to see this week's deals.
          </p>

        ) : dealsLoading ? (
          <p>
            Loading this week's deals...
          </p>

        ) : dealsError ? (
          <p className="error-message">
            {dealsError}
          </p>

        ) : deals.length === 0 ? (
          <p>
            No deals are currently available for this store.
          </p>

        ) : (
          <div className="deal-grid">
            {deals.slice(0, 6).map((deal) => (
              <div
                className="deal-card"
                key={deal.id}
              >
                <h3>{deal.item}</h3>
                <p>${deal.price}</p>
              </div>
            ))}
          </div>
        )}

      </section>

      <section className="planner">
        <h2>Turn these deals into meals</h2>

        <div className="planner-controls">
          <label>
            Number of meals:

            <input
              type="number"
              min="1"
              max="14"
              value={meals}
              onChange={(event) =>
                setMeals(Number(event.target.value))
              }
            />
          </label>
        </div>

        <button
          className="generate-button"
          onClick={generateMealPlan}
          disabled={
            mealPlanLoading ||
            dealsLoading ||
            !selectedStore ||
            deals.length === 0 ||
            meals < 1 ||
            meals > 14
          }
        >
          {dealsLoading
            ? "Loading Deals..."
            : mealPlanLoading
              ? "Building Your Meal Plan..."
              : "Build My Meal Plan"}
        </button>

        {mealPlanError && (
          <p className="error-message">
            {mealPlanError}
          </p>
        )}

      </section>

    </div>
  )
}

export default HomePage