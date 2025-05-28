'use client';

import { useEffect, useState } from 'react';

type Odds = {
  teams?: string[];
  bookmakers?: {
    title?: string;
    markets?: {
      key?: string;
      outcomes?: {
        name?: string;
        price?: number;
      }[];
    }[];
  }[];
};

type Prop = {
  [key: string]: string;
};

type MatchupSummary = {
  game: string;
  batters: {
    name: string;
    pitcher: string;
    stats: {
      PA: number;
      Hits: number;
      HR: number;
      K: number;
      BB: number;
    };
  }[];
};

export default function Home() {
  const [odds, setOdds] = useState<Odds[]>([]);
  const [props, setProps] = useState<Prop[]>([]);
  const [matchups, setMatchups] = useState<MatchupSummary[]>([]);
  const [tab, setTab] = useState('matchups');

  useEffect(() => {
    const fetchOdds = async () => {
      try {
        const res = await fetch('/api/odds');
        const data = await res.json();
        setOdds(data || []);
      } catch (e) {
        console.error('Failed to fetch odds', e);
      }
    };

    const fetchProps = async () => {
      try {
        const res = await fetch('/api/props');
        const data = await res.json();
        setProps(data || []);
      } catch (e) {
        console.error('Failed to fetch props', e);
      }
    };

    const fetchMatchups = async () => {
      try {
        const res = await fetch('/api/matchups');
        const data = await res.json();
        setMatchups(data || []);
      } catch (e) {
        console.error('Failed to fetch matchups', e);
      }
    };

    fetchOdds();
    fetchProps();
    fetchMatchups();
  }, []);

  return (
    <main className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center">MLB Betting Dashboard</h1>

      <div className="flex justify-center space-x-4 mb-6">
        <button onClick={() => setTab('matchups')} className={tab === 'matchups' ? 'font-bold underline' : ''}>
          Today’s Matchups
        </button>
        <button onClick={() => setTab('props')} className={tab === 'props' ? 'font-bold underline' : ''}>
          Top Props
        </button>
        <button onClick={() => setTab('insights')} className={tab === 'insights' ? 'font-bold underline' : ''}>
          H2H Insights
        </button>
      </div>

      {tab === 'matchups' && (
        <section>
          <h2 className="text-xl font-semibold mb-2">Odds</h2>
          {odds.map((game, i) => (
            <div key={i} className="mb-4 p-4 border rounded">
              <h3 className="text-lg font-bold mb-2">
                {(game.teams && Array.isArray(game.teams)) ? game.teams.join(' vs ') : 'Unknown Teams'}
              </h3>
              {game.bookmakers?.map((book, j) => (
                <div key={j}>
                  <p className="font-semibold">{book.title || 'Unknown Bookmaker'}</p>
                  {book.markets?.map((market, k) => (
                    <div key={k}>
                      <p className="italic">{market.key || 'Unknown Market'}</p>
                      {market.outcomes?.map((o, l) => (
                        <div key={l} className="ml-4">
                          {o.name || 'Unknown Outcome'}: {o.price ?? 'N/A'}
                        </div>
                      ))}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          ))}
        </section>
      )}

      {tab === 'props' && (
        <section>
          <h2 className="text-xl font-semibold mb-2">Positive EV Player Props</h2>
          {props.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full border">
                <thead>
                  <tr>
                    {Object.keys(props[0] || {}).map((key) => (
                      <th key={key} className="border px-2 py-1">{key}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {props.map((row, i) => (
                    <tr key={i}>
                      {Object.values(row).map((val, j) => (
                        <td key={j} className="border px-2 py-1">{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p>No props data found.</p>
          )}
        </section>
      )}

      {tab === 'insights' && (
        <section>
          <h2 className="text-xl font-semibold mb-2">H2H Matchup Insights</h2>
          {matchups.length > 0 ? (
            matchups.map((game, i) => (
              <div key={i} className="mb-6 p-4 border rounded">
                <h3 className="text-lg font-bold mb-2">{game.game}</h3>
                {game.batters.map((batter, j) => (
                  <div key={j} className="mb-2">
                    <p className="font-semibold">
                      {batter.name} vs {batter.pitcher}
                    </p>
                    <ul className="ml-4 list-disc">
                      <li>PA: {batter.stats?.PA ?? 0}</li>
                      <li>Hits: {batter.stats?.Hits ?? 0}</li>
                      <li>HR: {batter.stats?.HR ?? 0}</li>
                      <li>BB: {batter.stats?.BB ?? 0}</li>
                      <li>K: {batter.stats?.K ?? 0}</li>
                    </ul>
                  </div>
                ))}
              </div>
            ))
          ) : (
            <p>No H2H data available.</p>
          )}
        </section>
      )}
    </main>
  );
}
