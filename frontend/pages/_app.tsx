// pages/_app.tsx
import type { AppProps } from "next/app";

import { CssBaseline } from "@mui/material";
import Head from "next/head";
import "../app/globals.css";
import NavBar from "@/components/NavBar";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <>
      <Head>
        <meta name="viewport" content="initial-scale=1, width=device-width" />
      </Head>
      <CssBaseline />
      <div style={{ paddingBottom: 64 }}>
        <Component {...pageProps} />
      </div>
      <NavBar />
    </>
  );
}
