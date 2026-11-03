import { Link, useLocation } from 'react-router-dom'

function MealPlanPage() {
  const location = useLocation()

  const mealPlan = location.state?.mealPlan
  const store = location.state?.store

  if (!mealPlan) {
    return (
      <div className="app">
        <Link to="/">← Back</Link>

        <h1>No Meal Plan Yet</h1>
        <p>Build a meal plan from the home page first.</p>

        <Link to="/">Go to Home</Link>
      </div>
    )
  }

  return (
    <div className="app">
      <Link to="/">← Back</Link>

      <div className="meal-plan-header">
        <h1>Your Meal Plan</h1>
        <p>Based on this week's deals at {store}</p>
      </div>

      <section className="recommended-meals">
        <h2>Recommended Meals</h2>

        {mealPlan.recipes.map((recipe, index) => (
          <div className="meal-card" key={index}>

            <div className="meal-card-header">
              <h3>{recipe.recipe}</h3>

              <span className="match-badge">
                {recipe.match_percentage.toFixed(0)}% match
              </span>
            </div>

            <p>
              Matched Deal Cost: ${recipe.total_cost.toFixed(2)}
            </p>

            <div className="missing-ingredients">
              <p>Still Needed</p>

              <div className="ingredient-tags">
                {recipe.missing.map((ingredient, ingredientIndex) => (
                  <span key={ingredientIndex}>
                    {ingredient}
                  </span>
                ))}
              </div>
            </div>

          </div>
        ))}
      </section>

      <section className="shopping-list">
        <h2>Shopping List</h2>

        {Object.entries(mealPlan.shopping_list).map(([name, item]) => (
          <div className="shopping-list-item" key={name}>
            <span>{name}</span>
            <span>
              {item.quantity} {item.unit}
            </span>
          </div>
        ))}
      </section>

    </div>
  )
}

export default MealPlanPage