import process from 'node:process';

const COINS = {
  bitcoin: 'Bitcoin (BTC)',
  ethereum: 'Ethereum (ETH)',
};

const CURRENCY = 'eur';

const API_URL = 'https://api.coingecko.com/api/v3/simple/price';

const ESC = String.fromCharCode(27); // ESC para códigos ANSI
const COLORS = {
  green: `${ESC}[32m`,
  red: `${ESC}[31m`,
  gray: `${ESC}[90m`,
  bold: `${ESC}[1m`,
  reset: `${ESC}[0m`,
};

function buildUrl() {
  const params = new URLSearchParams({
    ids: Object.keys(COINS).join(','),
    vs_currencies: CURRENCY,
    include_24hr_change: 'true',
    include_last_updated_at: 'true',
  });

  return `${API_URL}?${params}`;
}

async function fetchPrices() {
  const res = await fetch(buildUrl());

  if (!res.ok) {
    const detail = res.status === 429
      ? 'se ha superado el límite de peticiones de CoinGecko, espera un minuto'
      : await res.text();
    throw new Error(`CoinGecko respondió ${res.status} ${res.statusText} — ${detail}`);
  }

  return res.json();
}

const eurFormatter = new Intl.NumberFormat('es-ES', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 2,
});

function formatEUR(value) {
  return eurFormatter.format(value);
}

function formatChange(pct) {
  const sign = pct > 0 ? '+' : '';
  return `${sign}${pct.toFixed(2)} %`;
}

function trendOf(pct) {
  if (pct > 0) return '▲ sube';
  if (pct < 0) return '▼ baja';
  return '= igual';
}

function colorFor(pct) {
  if (pct > 0) return COLORS.green;
  if (pct < 0) return COLORS.red;
  return COLORS.gray;
}

function priceChange24h(currentPrice, pct) {
  // El precio de hace 24 h se deduce del porcentaje: actual = anterior * (1 + pct/100)
  const previous = currentPrice / (1 + pct / 100);
  return currentPrice - previous;
}

function render(data) {
  const rows = [];

  for (const [id, name] of Object.entries(COINS)) {
    const entry = data[id];
    if (!entry) {
      throw new Error(`La respuesta de CoinGecko no incluye datos para "${id}"`);
    }

    const price = entry[CURRENCY];
    const change = entry[`${CURRENCY}_24h_change`] ?? 0;

    rows.push({
      'Criptomoneda': name,
      'Precio (EUR)': formatEUR(price),
      'Cambio 24h (%)': formatChange(change),
      'Cambio 24h (EUR)': formatEUR(priceChange24h(price, change)),
      'Tendencia': trendOf(change),
    });
  }

  console.log(`\n${COLORS.bold}Precios de criptomonedas — fuente: CoinGecko${COLORS.reset}\n`);

  // console.table cuenta los caracteres de escape ANSI al calcular el ancho de
  // columna, así que la tabla se imprime sin color y el resaltado va debajo.
  console.table(rows);

  console.log(`${COLORS.bold}Variación en las últimas 24 horas:${COLORS.reset}`);
  for (const [id, name] of Object.entries(COINS)) {
    const change = data[id][`${CURRENCY}_24h_change`] ?? 0;
    const color = colorFor(change);
    console.log(
      `  ${trendOf(change)}  ${name.padEnd(16)} ${color}${formatChange(change)}${COLORS.reset}`,
    );
  }

  const updatedAt = data.bitcoin?.last_updated_at;
  if (updatedAt) {
    const fecha = new Date(updatedAt * 1000).toLocaleString('es-ES');
    console.log(`\n${COLORS.gray}Última actualización: ${fecha}${COLORS.reset}\n`);
  }
}

try {
  render(await fetchPrices());
} catch (err) {
  console.error(`${COLORS.red}Error al obtener los precios:${COLORS.reset} ${err.message}`);
  process.exit(1);
}
