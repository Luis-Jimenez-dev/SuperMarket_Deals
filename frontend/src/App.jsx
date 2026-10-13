import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [stores, setStores] = useState([])
  const [selectedStore, setSelectedStore] = useState('')
  const [deals, setDeals] = useState([])
  const [meals, setMeals] = useState(1)
  const [mealPlan, setMealPlan] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/stores')
      .then(response => response.json())
      .then(data => setStores(data))
  }, [])

  useEffect(() => {
    setMealPlan(null)

    if (selectedStore !== '') {
      fetch(`http://127.0.0.1:8000/stores/${selectedStore}/deals`)
        .then(response => response.json())
        .then(data => setDeals(data))
    } else {
      setDeals([])
    }
  }, [selectedStore])

  function generateMealPlan() {
    if (selectedStore === '' || meals <= 0) {
      return
    }

    fetch(
      `http://127.0.0.1:8000/stores/${selectedStore}/meal-plan?meals=${meals}`
    )
      .then(response => response.json())
      .then(data => setMealPlan(data))
  }

  return (
    <div className="app">
      <header>
      <h1>Grocery Meal Planner</h1>
      <p>Turn this week's grocery deals into meals.</p>
      </header>

      <section className='planner'>
        <h2>Plan your meals</h2>
        <div className='planner-controls'>
        <label>
          Store:
          <select
            value={selectedStore}
            onChange={event => setSelectedStore(event.target.value)}
          >
            <option value="">Select a Store</option>

            {stores.map(store => (
              <option key={store.id} value={store.name}>
                {store.name}
              </option>
            ))}
          </select>
        </label>

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
          className='generate-button' 
          onClick={generateMealPlan}
        >
          Generate Meal Plan
        </button>
      </section>

      <h2>Weekly Deals</h2>
      {deals.map((deal, index) => (
        <p key={index}>
          {deal.item} - ${deal.price} {deal.unit}
        </p>
      ))}

      {mealPlan && (
        <div>
          <h2>Recommended Meals</h2>

          {mealPlan.recipes.map((recipe, index) => (
            <div className='meal-card' key={index}>
              <h3>{recipe.recipe}</h3>
              <h4>Deal Match: {recipe.match_percentage.toFixed(0)}%</h4>
              <p>
                Matched Deal Cost: ${recipe.total_cost.toFixed(2)}
              </p>
              <p>
                Need to Buy: {recipe.missing.join(', ')}
              </p>
            </div>
          ))}

          <div>
            <h2>Shopping List</h2>

            {Object.entries(mealPlan.shopping_list).map(([name, item]) => (
              <p key={name}>
                {name} - {item.quantity} {item.unit}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default App