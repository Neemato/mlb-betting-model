// File: src/app/api/odds/route.ts

import { NextResponse } from 'next/server';

export async function GET() {
  const apiKey = '6657287b46d7ec576e25e6c1bd2984c9';
  const url = `https://api.the-odds-api.com/v4/sports/baseball_mlb/odds?regions=us&markets=h2h,spreads,totals&oddsFormat=american&apiKey=${apiKey}`;

  try {
    const res = await fetch(url);
    if (!res.ok) {
      throw new Error(`API request failed with status ${res.status}`);
    }

    const data = await res.json();

    const formatted = data.map((game: any) => {
      const { home_team, away_team, commence_time, bookmakers } = game;
      const formattedBookmakers = bookmakers.map((book: any) => ({
        name: book.title,
        markets: book.markets.map((market: any) => ({
          key: market.key,
          outcomes: market.outcomes
        }))
      }));

      return {
        home_team,
        away_team,
        commence_time,
        bookmakers: formattedBookmakers
      };
    });

    return NextResponse.json(formatted);
  } catch (error) {
    console.error("Failed to fetch odds:", error);
    return NextResponse.json({ error: "Failed to fetch odds" }, { status: 500 });
  }
}
