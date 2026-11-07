import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const API_URL = 'http://127.0.0.1:8000'

function HomePage() {
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)

  const [postalCode, setPostalCode] = useState(() => {
    return localStorage.getItem('postalCode') ?? ''
  })

  const [nearbyStores, setNearbyStores] = useState([])

  const [selectedStore, setSelectedStore] = useState(() => {
    const savedStore = localStorage.getItem('selectedStore')

    return savedStore
      ? JSON.parse(savedStore)
      : null
  })

  const [dealsLoading, setDealsLoading] = useState(
    () => selectedStore !== null
  )

  const [mealPlanLoading, setMealPlanLoading] = useState(false)

  const [storeSearchError, setStoreSearchError] = useState('')
  const [dealsError, setDealsError] = useState('')
  const [mealPlanError, setMealPlanError] = useState('')

  const navigate = useNavigate()

  async function getErrorMessage(response, fallbackMessage) {
    try {
      const errorData = await response.json()
      return errorData.detail || fallbackMessage
    } catch {
      return fallbackMessage
    }
  }

  const findNearbyStores = async () => {
    const cleanedPostalCode = postalCode.trim()

    setStoreSearchError('')
    setNearbyStores([])

    if (!/^\d{5}$/.test(cleanedPostalCode)) {
      setStoreSearchError('Enter a valid 5-digit ZIP code.')
      return
    }

    try {
      const response = await fetch(
        `${API_URL}/stores/nearby?postal_code=${encodeURIComponent(cleanedPostalCode)}`
      )

      if (!response.ok) {
        const message = await getErrorMessage(
          response,
          'Unable to find nearby stores.'
        )

        throw new Error(message)
      }

      const data = await response.json()

      setNearbyStores(data)
      localStorage.setItem('postalCode', cleanedPostalCode)
      setPostalCode(cleanedPostalCode)

    } catch (error) {
      console.error('Failed to find nearby stores:', error)

      setStoreSearchError(
        error instanceof Error
          ? error.message
          : 'Unable to find nearby stores.'
      )
    }
  }

  const selectStore = (store) => {
    setDealsLoading(true)
    setDeals([])
    setDealsError('')
    setMealPlanError('')
    setSelectedStore(store)

    localStorage.setItem(
      'selectedStore',
      JSON.stringify(store)
    )
  }

  const changeStore = () => {
    setSelectedStore(null)
    setDeals([])
    setNearbyStores([])
    setDealsLoading(false)
    setDealsError('')
    setMealPlanError('')

    localStorage.removeItem('selectedStore')

    if (postalCode) {
      findNearbyStores()
    }
  }

  useEffect(() => {
    if (!selectedStore) {
      return
    }

    fetch(
      `${API_URL}/stores/${selectedStore.store_id}/deals`
    )
      .then(async response => {
        if (!response.ok) {
          const message = await getErrorMessage(
            response,
            'Unable to load deals.'
          )

          throw new Error(message)
        }

        return response.json()
      })
      .then(data => {
        setDeals(data)
      })
      .catch(error => {
        console.error('Failed to load deals:', error)

        setDealsError(
          error instanceof Error
            ? error.message
            : 'Unable to load deals.'
        )
      })
      .finally(() => {
        setDealsLoading(false)
      })

  }, [selectedStore])

  async function generateMealPlan() {
    if (
      !selectedStore ||
      meals < 1 ||
      meals > 14 ||
      dealsLoading ||
      deals.length === 0
    ) {
      return
    }

    setMealPlanError('')
    setMealPlanLoading(true)

    try {
      const response = await fetch(
        `${API_URL}/stores/${selectedStore.store_id}/meal-plan?meals=${meals}`
      )

      if (!response.ok) {
        const message = await getErrorMessage(
          response,
          'Unable to build a meal plan.'
        )

        throw new Error(message)
      }

      const data = await response.json()

      navigate('/meal-plan', {
        state: {
          mealPlan: data,
          store: selectedStore,
        },
      })

    } catch (error) {
      console.error('Failed to generate meal plan:', error)

      setMealPlanError(
        error instanceof Error
          ? error.message
          : 'Unable to build a meal plan.'
      )

    } finally {
      setMealPlanLoading(false)
    }
  }

  return (
    <div className="app">
      {selectedStore ? (
        <section className="store-info">
          <p className="store-label">Shopping at</p>

          <h2 className="store-name">
            {selectedStore.name}
          </h2>

          {selectedStore.city && (
            <p className="store-location">
              {selectedStore.city}
              {selectedStore.state && `, ${selectedStore.state}`}
            </p>
          )}

          {dealsLoading ? (
            <p className="store-deal-count">
              Loading this week's deals...
            </p>
          ) : dealsError ? (
            <p className="store-deal-count">
              Deals unavailable
            </p>
          ) : (
            <p className="store-deal-count">
              {deals.length === 1
                ? '1 deal found'
                : `${deals.length} deals found`}
            </p>
          )}

          <button
            type="button"
            className="secondary-button"
            onClick={changeStore}
            disabled={dealsLoading}
          >
            Change Store
          </button>
        </section>
      ) : (
        <section className="store-search">
          <h1>Find your weekly deals</h1>

          <p className="section-description">
            Enter your ZIP code to find a store near you.
          </p>

          <div className="store-search-controls">
            <input
              type="text"
              inputMode="numeric"
              value={postalCode}
              maxLength={5}
              placeholder="ZIP code"
              aria-label="ZIP code"
              onChange={(event) => {
                const value = event.target.value
                  .replace(/\D/g, '')
                  .slice(0, 5)

                setPostalCode(value)
              }}
            />

            <button
              type="button"
              className="primary-button"
              onClick={findNearbyStores}
            >
              Find Stores
            </button>
          </div>

          {storeSearchError && (
            <p className="error-message">
              {storeSearchError}
            </p>
          )}

          {nearbyStores.length > 0 && (
            <select
              className="store-select"
              defaultValue=""
              aria-label="Choose a nearby store"
              onChange={(event) => {
                const store = nearbyStores.find(
                  store =>
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

              {nearbyStores.map(store => (
                <option
                  key={store.store_id}
                  value={store.store_id}
                >
                  {store.name}
                  {store.distance != null &&
                    ` — ${Number(store.distance).toFixed(1)} miles`}
                </option>
              ))}
            </select>
          )}
        </section>
      )}

      <section className="weekly-deals-preview">
        <div className="section-header">
          <div>
            <h2>Weekly Deals</h2>
            <p className="section-description">
              See what's on sale at your selected store.
            </p>
          </div>

          {selectedStore &&
            !dealsLoading &&
            !dealsError &&
            deals.length > 0 && (
              <Link
                className="section-link"
                to="/deals"
              >
                View All Deals
              </Link>
            )}
        </div>

        {!selectedStore ? (
          <p>Select a store to see this week's deals.</p>
        ) : dealsLoading ? (
          <p>Loading this week's deals...</p>
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
            {deals.slice(0, 6).map(deal => (
              <article
                className="deal-card"
                key={deal.id}
              >
                <h3 className="deal-name">
                  {deal.item}
                </h3>

                {deal.price != null && (
                  <p className="deal-price">
                    ${Number(deal.price).toFixed(2)}
                  </p>
                )}

                {deal.promotion && (
                  <p className="deal-promotion">
                    {deal.promotion}
                  </p>
                )}
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="planner">
        <div className="planner-content">
          <div>
            <h2>Turn these deals into meals</h2>

            <p className="section-description">
              Build a meal plan around ingredients currently on sale.
            </p>
          </div>

          <div className="planner-actions">
            <div className="planner-controls">
              <label>
                Number of meals

                <input
                  type="number"
                  min="1"
                  max="14"
                  value={meals}
                  onChange={(event) => {
                    setMeals(Number(event.target.value))
                  }}
                />
              </label>
            </div>

            <button
              type="button"
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
                ? 'Loading Deals...'
                : mealPlanLoading
                  ? 'Building Your Meal Plan...'
                  : 'Build My Meal Plan'}
            </button>
          </div>
        </div>

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