import { useEffect, useState } from 'react'

function App() {
  const [trends, setTrends] = useState([])

  useEffect(() => {
    fetch('/trending.json')
      .then(res => res.json())
      .then(data => setTrends(data))
  }, [])

  return (
    <div className="min-h-screen bg-black text-white p-6">
      <h1 className="text-3xl font-bold text-center mb-8">🔥 Trending Keywords</h1>
      <div className="max-w-2xl mx-auto space-y-4">
        {trends.length === 0 ? (
          <p className="text-center text-gray-400">No data yet. Run scraper to generate trending.json</p>
        ) : (
          trends.map((item, index) => (
            <div key={index} className="bg-gray-800 p-4 rounded-lg">
              <h2 className="text-xl font-semibold capitalize">{item.keyword}</h2>
              <p>Mentions: {item.mentions}</p>
              <p>Upvotes: {item.upvotes}</p>
              <p className="text-green-400">Momentum Score: {item.score}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default App
