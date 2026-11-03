import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function HomePage() {
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()

  useEffect(() => {
    fetch('http://127.0.0.1:8000/stores/Safeway Broadway/deals')
      .then(response => response.json())
      .then(data => setDeals(data))
  }, [])

  function generateMealPlan() {
    if (meals <= 0) {
      return
    }

    setLoading(true)

    fetch(
      `http://127.0.0.1:8000/stores/Safeway Broadway/meal-plan?meals=${meals}`
    )
      .then(response => response.json())
      .then(data => {
        navigate('/meal-plan', {
          state: {
            mealPlan: data,
            store: 'Safeway Broadway'
          }
        })
      })
      .catch(error => {
        console.error('Failed to generate meal plan:', error)
      })
      .finally(() => {
        setLoading(false)
      })
  }

  return (
    <div className="app">

      <section className="store-info">
        <h2>Safeway Broadway</h2>
        <p>Oakland, CA</p>
        <p>{deals.length} deals found</p>
      </section>

      <section className="weekly-deals-preview">
        <div className="section-header">
          <h2>Weekly Deals</h2>
          <Link to="/deals">View All Deals</Link>
        </div>

        <div className="deal-grid">
          {deals.slice(0, 6).map((deal, index) => (
            <div className="deal-card" key={index}>
              <h3>{deal.item}</h3>
              <p>${deal.price}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="planner">
        <h2>Turn these deals into meals</h2>

        <div className="planner-controls">
          <label>
            Number of meals:
            <input
              type="number"
              min="1"
              value={meals}
              onChange={event => setMeals(event.target.value)}
            />
          </label>
        </div>

        <button
          className="generate-button"
          onClick={generateMealPlan}
          disabled={loading}
        >
          {loading ? 'Building Your Meal Plan...' : 'Build My Meal Plan'}
        </button>
      </section>

    </div>
  )
}

export default HomePage