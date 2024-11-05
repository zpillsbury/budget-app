import { useEffect, useState } from "react"
import "./App.css"

interface Moneybudget {
  id: string
  budget: number
  created_at: string
  updated_at: string | null
}

export function App() {
  const [budgets, setBudgets] = useState<Moneybudget[]>([])
  const [money, setMoney] = useState("")

  useEffect(() => {
    async function getBudgets() {
      const response = await fetch("http://localhost:8000/v1/budgets", {
        method: "GET",
      })

      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      }

      const data = await response.json()
      setBudgets(data)
    }

    getBudgets()
  }, [])

  async function addBudget() {
    const send = await fetch("http://localhost:8000/v1/budgets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        budget: money,
      }),
    })

    if (!send.ok) {
      throw new Error(`Send status: ${send.status}`)
    }
  }

  return (
    <>
      <h1>Budgets</h1>
      <div>
        <input value={money} type="number" onChange={(e) => setMoney(e.target.value)} />
        <button onClick={addBudget}>Add Budget</button>
      </div>

      <div className="card">
        {budgets.reverse().map((budget) => (
          <p key={budget.id}>{budget.budget}</p>
        ))}
      </div>
    </>
  )
}

export default App
