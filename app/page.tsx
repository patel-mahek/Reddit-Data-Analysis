"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from "recharts"
import { Button } from "@/components/ui/button"

// Add this mock data for misleading posts at the top of the file, after the existing mock data
const misleadingPosts = [
  {
    id: 1,
    title: "Scientists Discover Revolutionary Weight Loss Method",
    upvoteRatio: 0.67,
    comments: 342,
    selfText:
      "This groundbreaking research claims to have found a way to lose weight without diet or exercise, but the study was funded by a supplement company and used a very small sample size.",
    subreddit: "r/health",
    authorName: "health_guru_123",
    url: "https://example.com/fake-weight-loss",
  },
  {
    id: 2,
    title: "Breaking: Government Admits to Alien Contact",
    upvoteRatio: 0.82,
    comments: 1205,
    selfText:
      "An anonymous source claims government officials have been in contact with extraterrestrial beings for decades, but provides no verifiable evidence or credible sources.",
    subreddit: "r/conspiracy",
    authorName: "truth_seeker_42",
    url: "https://example.com/alien-conspiracy",
  },
  {
    id: 3,
    title: "New Study Shows Chocolate Cures Cancer",
    upvoteRatio: 0.73,
    comments: 567,
    selfText:
      "The headline drastically overstates the findings of a preliminary study that only showed a minor correlation between a specific compound in dark chocolate and reduced cancer cell growth in a petri dish.",
    subreddit: "r/science",
    authorName: "choco_lover",
    url: "https://example.com/chocolate-research",
  },
  {
    id: 4,
    title: "Tech CEO Announces Revolutionary AI That Passes Turing Test",
    upvoteRatio: 0.91,
    comments: 876,
    selfText:
      "The announcement fails to mention that the test was conducted under very specific conditions with carefully selected questions, and independent experts have not verified the claims.",
    subreddit: "r/technology",
    authorName: "future_tech_fan",
    url: "https://example.com/ai-breakthrough",
  },
  {
    id: 5,
    title: "Celebrity Reveals Secret to Eternal Youth",
    upvoteRatio: 0.62,
    comments: 423,
    selfText:
      "The article is essentially an advertisement for an expensive skincare line without any scientific evidence for the extraordinary claims being made about its effectiveness.",
    subreddit: "r/entertainment",
    authorName: "celeb_news_daily",
    url: "https://example.com/celebrity-skincare",
  },
]


const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884D8", "#82ca9d"]
function MisleadingPostCard() {
  const [currentIndex, setCurrentIndex] = useState(0)

  const nextPost = () => {
    setCurrentIndex((prevIndex) => (prevIndex === misleadingPosts.length - 1 ? 0 : prevIndex + 1))
  }

  const prevPost = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? misleadingPosts.length - 1 : prevIndex - 1))
  }

  const post = misleadingPosts[currentIndex]

  return (
    <Card className="w-full overflow-hidden">
      <CardHeader className="bg-muted/50 pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg">Misleading Post Analysis</CardTitle>
          <div className="text-sm text-muted-foreground">
            {currentIndex + 1} of {misleadingPosts.length}
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-6">
        <div className="space-y-4">
          <div>
            <h3 className="text-xl font-bold line-clamp-2">{post.title}</h3>
            <div className="flex flex-wrap gap-2 mt-2">
              <div className="text-sm bg-secondary px-2 py-1 rounded-md">{post.subreddit}</div>
              <div className="text-sm bg-secondary px-2 py-1 rounded-md">by {post.authorName}</div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 py-2">
            <div className="text-center">
              <div className="text-2xl font-bold">{post.upvoteRatio * 100}%</div>
              <div className="text-xs text-muted-foreground">Upvote Ratio</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">{post.comments}</div>
              <div className="text-xs text-muted-foreground">Comments</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold">
                {post.upvoteRatio > 0.8 ? "High" : post.upvoteRatio > 0.7 ? "Medium" : "Low"}
              </div>
              <div className="text-xs text-muted-foreground">Credibility</div>
            </div>
          </div>

          <div className="bg-muted/30 p-3 rounded-md">
            <p className="text-sm line-clamp-4">{post.selfText}</p>
          </div>

          <div className="text-sm truncate">
            <span className="text-muted-foreground">Source: </span>
            <a href={post.url} className="text-primary hover:underline truncate">
              {post.url}
            </a>
          </div>
        </div>
      </CardContent>
      <div className="flex border-t">
        <Button variant="ghost" className="flex-1 rounded-none h-12" onClick={prevPost}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="mr-2 h-4 w-4"
          >
            <path d="m15 18-6-6 6-6" />
          </svg>
          Previous
        </Button>
        <div className="w-px bg-border h-12" />
        <Button variant="ghost" className="flex-1 rounded-none h-12" onClick={nextPost}>
          Next
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="ml-2 h-4 w-4"
          >
            <path d="m9 18 6-6-6-6" />
          </svg>
        </Button>
      </div>
    </Card>
  )
}

export default function Dashboard() {
  const [metricType, setMetricType] = useState("posts")
  const [chartType, setChartType] = useState("bar")
  const [accountsData, setAccountsData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [monthlyTrends, setMonthlyTrends] = useState([])
  const [filteredKeywords, setFilteredKeywords] = useState([])
  const [selectedMonth, setSelectedMonth] = useState("")


  // Prepare data for pie chart
  const pieData = accountsData.map((item) => ({
    name: item.name,
    value: item[metricType as keyof typeof item],
  }))

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [engagementRes, trendsRes] = await Promise.all([
          fetch("http://127.0.0.1:8000/engagement-metrics"),
          fetch("http://127.0.0.1:8000/trending-keyword-counts")
        ])
  
        if (!engagementRes.ok || !trendsRes.ok) throw new Error("Failed to fetch data")
  
        const engagementData = await engagementRes.json()
        const trendsData = await trendsRes.json()
  
        // Convert engagement data to array format
        const formattedEngagement = Object.entries(engagementData).map(([name, values]) => ({
          name,
          ...values,
        }))
        setMonthlyTrends(trendsData)
          if (trendsData.length > 0) {
            setSelectedMonth(trendsData[0].month) // Default to first available month
          }
        setAccountsData(formattedEngagement)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
  
    fetchData()
  }, [])

  useEffect(() => {
    if (selectedMonth) {
      const filtered = monthlyTrends.filter((item) => item.month === selectedMonth)
      setFilteredKeywords(filtered)
    }
  }, [selectedMonth, monthlyTrends])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>


  return (
    <div className="container mx-auto py-6 space-y-6">
      

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>Total Posts</CardTitle>
            <CardDescription>Number of posts across all accounts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">{accountsData.reduce((sum, account) => sum + account.posts, 0)}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Comments</CardTitle>
            <CardDescription>Number of comments across all accounts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">{accountsData.reduce((sum, account) => sum + account.comments, 0)}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Total Upvotes</CardTitle>
            <CardDescription>Number of upvotes across all accounts</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold">{accountsData.reduce((sum, account) => sum + account.upvotes, 0)}</div>
          </CardContent>
        </Card>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
        <div className="flex flex-col sm:flex-row items-right gap-2">
          <div className="w-40">
            <Select value={metricType} onValueChange={(value) => setMetricType(value)}>
              <SelectTrigger>
                <SelectValue placeholder="Select metric" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="posts">Posts</SelectItem>
                <SelectItem value="comments">Comments</SelectItem>
                <SelectItem value="upvotes">Upvotes</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="w-40">
            <Select value={chartType} onValueChange={(value) => setChartType(value)}>
              <SelectTrigger>
                <SelectValue placeholder="Chart type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="bar">Bar Chart</SelectItem>
                <SelectItem value="pie">Pie Chart</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <Card className="col-span-full">
        <CardHeader>
          <CardTitle>Account {metricType.charAt(0).toUpperCase() + metricType.slice(1)} Comparison</CardTitle>
          <CardDescription>Compare {metricType} across different accounts</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] w-full">
            {chartType === "bar" && (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={accountsData}
                  margin={{
                    top: 20,
                    right: 30,
                    left: 20,
                    bottom: 60,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={60} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey={metricType} fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            )}

            {chartType === "pie" && (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={true}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={150}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value} ${metricType}`, ""]} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            )}

          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
      <div className="container mx-auto py-6 space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Keyword Trends</h1>
          <p className="text-muted-foreground">Analyze trending keywords over time</p>
        </div>
        <div className="w-40">
          <Select value={selectedMonth} onValueChange={(value) => setSelectedMonth(value)}>
            <SelectTrigger>
              <SelectValue placeholder="Select Month" />
            </SelectTrigger>
            <SelectContent>
              {Array.from(new Set(monthlyTrends.map((item) => item.month))).map((month) => (
                <SelectItem key={month} value={month}>{month}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <Card className="col-span-full">
        {/* <CardHeader>
          <CardTitle>Keyword Frequency for {selectedMonth}</CardTitle>
          <CardDescription>Trending keywords and their occurrence</CardDescription>
        </CardHeader> */}
        <CardContent>
          <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={filteredKeywords}
                margin={{ top: 20, right: 30, left: 20, bottom: 60 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="keyword" angle={-45} textAnchor="end" height={60} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#8884d8" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
        <Card>
          <CardHeader>
            <CardTitle>Top Performers</CardTitle>
            <CardDescription>Accounts with highest {metricType}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[...accountsData]
                .sort((a, b) => b[metricType as keyof typeof b] - a[metricType as keyof typeof a])
                .slice(0, 5)
                .map((account, index) => (
                  <div key={account.name} className="flex items-center">
                    <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground mr-3">
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <div className="text-sm font-medium">{account.name}</div>
                      <div className="h-2 bg-muted rounded-full mt-1">
                        <div
                          className="h-2 bg-primary rounded-full"
                          style={{
                            width: `${
                              (account[metricType as keyof typeof account] /
                                Math.max(...accountsData.map((a) => a[metricType as keyof typeof a]))) *
                              100
                            }%`,
                          }}
                        />
                      </div>
                    </div>
                    <div className="ml-3 font-medium">{account[metricType as keyof typeof account]}</div>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      </div>
      <MisleadingPostCard />
    </div>
  )
}

