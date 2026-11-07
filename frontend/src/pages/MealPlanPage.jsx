import { Link, useLocation } from 'react-router-dom'

function MealPlanPage() {
  const location = useLocation()

  const mealPlan = location.state?.mealPlan
  const store = location.state?.store

  if (!mealPlan) {
    return (
      <div className="app empty-page">
        <Link className="back-link" to="/">
          ← Back
        </Link>

        <h1>No Meal Plan Yet</h1>

        <p>
          Build a meal plan from the home page first.
        </p>

        <Link className="primary-link" to="/">
          Go to Home
        </Link>
      </div>
    )
  }

  const recipes = mealPlan.recipes ?? []
  const shoppingList = mealPlan.shopping_list ?? {}

  return (
    <div className="app">
      <Link className="back-link" to="/">
        ← Back
      </Link>

      <header className="meal-plan-header">
        <p className="page-eyebrow">
          Meal Planner
        </p>

        <h1>Your Meal Plan</h1>

        {store && (
          <p>
            Based on this week's deals at {store.name}
            {store.city &&
              ` · ${store.city}${store.state
                ? `, ${store.state}`
                : ''}`}
          </p>
        )}
      </header>

      <section className="recommended-meals">
        <h2>Recommended Meals</h2>

        {recipes.length > 0 ? (
          recipes.map((recipe) => (
            <article
              className="meal-card"
              key={recipe.recipe_id}
            >
              <div className="meal-card-top">
                {recipe.image_url && (
                  <div className="meal-image-container">
                    <img
                      className="meal-image"
                      src={recipe.image_url}
                      alt={recipe.recipe}
                      loading="lazy"
                    />
                  </div>
                )}

                <div className="meal-card-summary">
                  <div className="meal-card-header">
                    <div>
                      <h3>{recipe.recipe}</h3>

                      {(recipe.category || recipe.cuisine) && (
                        <p className="meal-details">
                          {[recipe.category, recipe.cuisine]
                            .filter(Boolean)
                            .join(' · ')}
                        </p>
                      )}
                    </div>

                    <span className="match-badge">
                      {recipe.match_percentage?.toFixed(0)}% match
                    </span>
                  </div>

                  <p className="match-summary">
                    {recipe.matches}{' '}
                    {recipe.matches === 1
                      ? 'ingredient'
                      : 'ingredients'}{' '}
                    on sale
                  </p>
                </div>
              </div>

              <div className="matched-ingredients">
                <h4>On Sale</h4>

                {recipe.matched_deals?.length > 0 ? (
                  recipe.matched_deals.map((deal, index) => (
                    <div
                      className="matched-deal"
                      key={`${deal.canonical_ingredient}-${deal.item}-${index}`}
                    >
                      <div>
                        <strong>
                          ✓ {deal.ingredient?.name}
                        </strong>

                        {deal.ingredient?.measurement && (
                          <span className="ingredient-measurement">
                            {' '}
                            · {deal.ingredient.measurement}
                          </span>
                        )}
                      </div>

                      <div className="matched-product">
                        <span>{deal.item}</span>

                        {deal.price != null && (
                          <strong>
                            ${Number(deal.price).toFixed(2)}
                          </strong>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <p>No matching deals found.</p>
                )}
              </div>

              <div className="missing-ingredients">
                <h4>Still Needed</h4>

                <div className="ingredient-tags">
                  {recipe.missing_ingredients?.length > 0 ? (
                    recipe.missing_ingredients.map((ingredient) => (
                      <span
                        key={`${recipe.recipe_id}-${ingredient.name}`}
                      >
                        {ingredient.name}

                        {ingredient.measurement &&
                          ` · ${ingredient.measurement}`}
                      </span>
                    ))
                  ) : (
                    <span>
                      No additional ingredients needed
                    </span>
                  )}
                </div>
              </div>
            </article>
          ))
        ) : (
          <p>
            No matching meals were found for this week's deals.
          </p>
        )}
      </section>

      <section className="shopping-list">
        <h2>Shopping List</h2>

        {Object.keys(shoppingList).length > 0 ? (
          Object.entries(shoppingList).map(([name, item]) => (
            <div
              className="shopping-list-item"
              key={name}
            >
              <span>{name}</span>

              <span>
                {item.measurement || 'Quantity not specified'}
              </span>
            </div>
          ))
        ) : (
          <p>
            No additional ingredients are needed.
          </p>
        )}
      </section>
    </div>
  )
}

export default MealPlanPage