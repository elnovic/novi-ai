'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import dynamic from 'next/dynamic'

const CarteMondeComponent = dynamic(() => import('@/components/CarteMonde'), {
  ssr: false,
  loading: () => (
    <div className="h-full flex items-center justify-center bg-gray-50 rounded-2xl">
      <div className="text-center">
        <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm text-gray-400">Chargement de la carte...</p>
      </div>
    </div>
  )
})

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const scoreColor = (score: number) => {
  if (score >= 90) return "text-green-600 bg-green-50"
  if (score >= 75) return "text-blue-600 bg-blue-50"
  if (score >= 60) return "text-amber-600 bg-amber-50"
  return "text-red-500 bg-red-50"
}

// Données statiques de fallback
const donneesFallback: Record<string, any> = {
  "Maroc": { drapeau: "🇲🇦", lat: 31.7917, lng: -7.0926, score: 78, tendances: ["IA & Fintech", "Smart Cities", "Énergies renouvelables"], startups: "340+", investissement: "2.1 Mds $", resume: "Le Maroc développe activement son écosystème tech.", actualites: [] },
  "Sénégal": { drapeau: "🇸🇳", lat: 14.4974, lng: -14.4524, score: 65, tendances: ["Agritech", "Mobile Banking", "Éducation numérique"], startups: "180+", investissement: "450 M $", resume: "Le Sénégal mise sur la transformation digitale.", actualites: [] },
  "France": { drapeau: "🇫🇷", lat: 46.2276, lng: 2.2137, score: 92, tendances: ["IA Générative", "Quantique", "Cybersécurité"], startups: "4 200+", investissement: "12.4 Mds $", resume: "La France est un leader européen de l'IA.", actualites: [] },
  "Nigeria": { drapeau: "🇳🇬", lat: 9.0820, lng: 8.6753, score: 71, tendances: ["Fintech", "IA Santé", "E-commerce"], startups: "890+", investissement: "3.2 Mds $", resume: "Le Nigeria est la Silicon Valley africaine.", actualites: [] },
  "USA": { drapeau: "🇺🇸", lat: 37.0902, lng: -95.7129, score: 99, tendances: ["AGI", "IA Générative", "Quantique"], startups: "45 000+", investissement: "340 Mds $", resume: "Les USA dominent l'IA mondiale.", actualites: [] },
  "Chine": { drapeau: "🇨🇳", lat: 35.8617, lng: 104.1954, score: 97, tendances: ["IA Générative", "Semi-conducteurs", "Robotique"], startups: "12 000+", investissement: "95 Mds $", resume: "La Chine rivalise avec les USA en IA.", actualites: [] },
  "Allemagne": { drapeau: "🇩🇪", lat: 51.1657, lng: 10.4515, score: 94, tendances: ["Industrie 4.0", "Robotique", "Voiture autonome"], startups: "3 800+", investissement: "18.7 Mds $", resume: "L'Allemagne excelle dans l'industrie 4.0.", actualites: [] },
  "Inde": { drapeau: "🇮🇳", lat: 20.5937, lng: 78.9629, score: 85, tendances: ["IA", "Fintech", "Space Tech"], startups: "11 000+", investissement: "28 Mds $", resume: "L'Inde est une puissance tech émergente.", actualites: [] },
  "Rwanda": { drapeau: "🇷🇼", lat: -1.9403, lng: 29.8739, score: 74, tendances: ["Smart Cities", "Drones médicaux", "Fintech"], startups: "120+", investissement: "280 M $", resume: "Le Rwanda est le modèle tech d'Afrique.", actualites: [] },
  "Japon": { drapeau: "🇯🇵", lat: 36.2048, lng: 138.2529, score: 91, tendances: ["Robotique", "IA", "Semiconducteurs"], startups: "5 600+", investissement: "15.3 Mds $", resume: "Le Japon reste leader mondial en robotique.", actualites: [] },
  "Brésil": { drapeau: "🇧🇷", lat: -14.2350, lng: -51.9253, score: 72, tendances: ["Agritech", "Fintech", "IA Santé"], startups: "4 300+", investissement: "8.5 Mds $", resume: "Le Brésil est le hub tech d'Amérique latine.", actualites: [] },
  "Canada": { drapeau: "🇨🇦", lat: 56.1304, lng: -106.3468, score: 90, tendances: ["IA", "CleanTech", "BioTech"], startups: "6 800+", investissement: "19.2 Mds $", resume: "Le Canada est un centre mondial de recherche IA.", actualites: [] },
  "Émirats Arabes Unis": { drapeau: "🇦🇪", lat: 23.4241, lng: 53.8478, score: 88, tendances: ["Smart Cities", "IA", "Blockchain"], startups: "1 200+", investissement: "7.8 Mds $", resume: "Les EAU investissent massivement dans l'IA.", actualites: [] },
  "Corée du Sud": { drapeau: "🇰🇷", lat: 35.9078, lng: 127.7669, score: 93, tendances: ["Semiconducteurs", "Robotique", "5G"], startups: "4 900+", investissement: "16.4 Mds $", resume: "La Corée du Sud domine les semiconducteurs.", actualites: [] }
}

export default function Innovation() {
  const [paysData, setPaysData] = useState<Record<string, any>>(donneesFallback)
  const [paysSelectionne, setPaysSelectionne] = useState<string | null>(null)
  const [recherche, setRecherche] = useState('')
  const [chargement, setChargement] = useState(true)
  const [derniereMaj, setDerniereMaj] = useState<string | null>(null)
  const [rafraichissement, setRafraichissement] = useState(false)

  useEffect(() => {
    chargerDonnees()
  }, [])

  const chargerDonnees = async () => {
    try {
      const res = await fetch(`${API_URL}/innovation`)
      const data = await res.json()

      if (data && data.length > 0) {
        const map: Record<string, any> = {}
        data.forEach((p: any) => {
          map[p.pays] = {
            drapeau: p.drapeau,
            lat: p.lat,
            lng: p.lng,
            score: p.score,
            tendances: p.tendances || [],
            resume: p.resume,
            actualites: p.actualites || [],
            startups: p.startups,
            investissement: p.investissement,
            updated_at: p.updated_at
          }
        })
        setPaysData({ ...donneesFallback, ...map })
        const dates = data.map((p: any) => p.updated_at).filter(Boolean)
        if (dates.length > 0) {
          setDerniereMaj(new Date(dates[0]).toLocaleDateString('fr-FR'))
        }
      }
    } catch (e) {
      console.log('API non disponible, utilisation des données locales')
    } finally {
      setChargement(false)
    }
  }

  const rafraichir = async () => {
    setRafraichissement(true)
    try {
      await fetch(`${API_URL}/innovation/rafraichir`, { method: 'POST' })
      await chargerDonnees()
    } catch (e) {
      console.error(e)
    } finally {
      setRafraichissement(false)
    }
  }

  const paysFiltres = Object.keys(paysData).filter(pays =>
    pays.toLowerCase().includes(recherche.toLowerCase()) ||
    paysData[pays].tendances?.some((t: string) => t.toLowerCase().includes(recherche.toLowerCase()))
  )

  const pays = paysSelectionne ? paysData[paysSelectionne] : null

  return (
    <main className="min-h-screen bg-white">

      {/* Header */}
      <div className="bg-gray-950 text-white px-8 py-12">
        <div className="max-w-7xl mx-auto">
          <Link href="/" className="text-sm text-gray-400 hover:text-white mb-6 inline-block">← Accueil</Link>
          <div className="flex items-start justify-between gap-6">
            <div>
              <h1 className="text-3xl font-bold mb-2">Novi Innovation</h1>
              <p className="text-gray-400">Carte mondiale des évolutions technologiques en temps réel</p>
              {derniereMaj && (
                <p className="text-xs text-gray-500 mt-2">Dernière mise à jour : {derniereMaj}</p>
              )}
            </div>
            <button onClick={rafraichir} disabled={rafraichissement}
              className="flex-shrink-0 flex items-center gap-2 bg-blue-600 text-white px-4 py-2.5 rounded-xl text-sm font-medium hover:bg-blue-700 disabled:opacity-50">
              {rafraichissement ? (
                <>
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Mise à jour...
                </>
              ) : (
                <>↺ Actualiser</>
              )}
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8">

        {/* Recherche */}
        <div className="mb-6">
          <input type="text" placeholder="Rechercher un pays ou une technologie..."
            value={recherche} onChange={e => setRecherche(e.target.value)}
            className="w-full max-w-md px-4 py-2.5 border-2 border-gray-200 rounded-xl text-sm focus:outline-none focus:border-blue-500" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6" style={{ height: '600px' }}>

          {/* Carte */}
          <div className="lg:col-span-2 rounded-2xl overflow-hidden border border-gray-100 h-full">
            {chargement ? (
              <div className="h-full flex items-center justify-center bg-gray-50">
                <div className="text-center">
                  <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3" />
                  <p className="text-sm text-gray-400">Chargement de la carte...</p>
                </div>
              </div>
            ) : (
              <CarteMondeComponent
                paysData={paysData}
                paysFiltres={paysFiltres}
                paysSelectionne={paysSelectionne}
                onPaysClick={(nom: string) => setPaysSelectionne(nom)}
              />
            )}
          </div>

          {/* Panel infos pays */}
          <div className="h-full overflow-y-auto space-y-4">
            {!pays ? (
              <div className="h-full flex flex-col">
                <div className="bg-gray-50 rounded-2xl border border-gray-100 p-6 text-center mb-4">
                  <span className="text-5xl mb-4 block">🌍</span>
                  <h3 className="font-semibold text-gray-900 mb-2">Explore le monde tech</h3>
                  <p className="text-sm text-gray-400">Clique sur un pays pour voir ses évolutions technologiques.</p>
                </div>

                {/* Top pays */}
                <div className="space-y-2 flex-1 overflow-y-auto">
                  <p className="text-xs font-medium text-gray-500 uppercase tracking-wider px-1">Top pays</p>
                  {Object.entries(paysData)
                    .sort(([, a], [, b]) => b.score - a.score)
                    .slice(0, 8)
                    .map(([nom, data]) => (
                      <button key={nom} onClick={() => setPaysSelectionne(nom)}
                        className="w-full flex items-center gap-3 p-3 bg-white rounded-xl border border-gray-100 hover:border-blue-200 transition-colors text-left">
                        <span className="text-xl">{data.drapeau}</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900">{nom}</p>
                          <p className="text-xs text-gray-400 truncate">{data.tendances?.[0]}</p>
                        </div>
                        <span className={`text-xs font-bold px-2 py-0.5 rounded-full flex-shrink-0 ${scoreColor(data.score)}`}>
                          {data.score}
                        </span>
                      </button>
                    ))}
                </div>
              </div>
            ) : (
              <div className="space-y-4">

                {/* Header pays */}
                <div className="bg-white border border-gray-100 rounded-2xl p-5">
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-4xl">{pays.drapeau}</span>
                    <div className="flex-1">
                      <h2 className="text-xl font-bold text-gray-900">{paysSelectionne}</h2>
                      <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${scoreColor(pays.score)}`}>
                        Score d'innovation : {pays.score}/100
                      </span>
                    </div>
                    <button onClick={() => setPaysSelectionne(null)}
                      className="text-gray-400 hover:text-gray-600 text-xl">×</button>
                  </div>

                  <p className="text-sm text-gray-600 leading-relaxed mb-4">{pays.resume}</p>

                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-50 rounded-xl p-3 text-center">
                      <p className="font-bold text-gray-900">{pays.startups}</p>
                      <p className="text-xs text-gray-400">Startups</p>
                    </div>
                    <div className="bg-gray-50 rounded-xl p-3 text-center">
                      <p className="font-bold text-gray-900 text-sm">{pays.investissement}</p>
                      <p className="text-xs text-gray-400">Investissement</p>
                    </div>
                  </div>
                </div>

                {/* Tendances */}
                <div className="bg-white border border-gray-100 rounded-2xl p-5">
                  <h3 className="font-semibold text-gray-900 mb-3 text-sm">Tendances tech</h3>
                  <div className="flex flex-wrap gap-2">
                    {pays.tendances?.map((t: string) => (
                      <span key={t} className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-full">{t}</span>
                    ))}
                  </div>
                </div>

                {/* Actualités réelles */}
                {pays.actualites?.length > 0 && (
                  <div className="bg-white border border-gray-100 rounded-2xl p-5">
                    <h3 className="font-semibold text-gray-900 mb-3 text-sm">
                      Actualités récentes
                      <span className="text-xs text-green-600 ml-2 font-normal">● En direct</span>
                    </h3>
                    <div className="space-y-3">
                      {pays.actualites.slice(0, 3).map((a: any, i: number) => (
                        <a key={i} href={a.url} target="_blank" rel="noopener noreferrer"
                          className="block bg-gray-50 rounded-xl p-3 hover:bg-blue-50 transition-colors">
                          <p className="text-xs font-medium text-gray-900 line-clamp-2 mb-1">{a.titre}</p>
                          <div className="flex items-center justify-between">
                            <span className="text-xs text-gray-400">{a.source}</span>
                            <span className="text-xs text-gray-400">{a.date}</span>
                          </div>
                        </a>
                      ))}
                    </div>
                  </div>
                )}

                {pays.actualites?.length === 0 && (
                  <div className="bg-amber-50 border border-amber-100 rounded-2xl p-4">
                    <p className="text-xs text-amber-700">
                      Les actualités en temps réel seront disponibles après la prochaine mise à jour.
                    </p>
                    <button onClick={rafraichir} disabled={rafraichissement}
                      className="text-xs text-amber-600 hover:underline mt-2 block">
                      Actualiser maintenant →
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}