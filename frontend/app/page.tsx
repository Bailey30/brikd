"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <button
          className={styles.secondary}
          type="button"
          onClick={() => router.push("/company")}
        >
          company
        </button>
        <button
          className={styles.secondary}
          type="button"
          onClick={() => router.push("/job-search")}
        >
          job
        </button>
      </main>
      <footer></footer>
    </div>
  );
}
