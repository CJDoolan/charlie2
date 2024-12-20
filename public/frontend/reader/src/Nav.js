import './css/nav_styles.css';
import React, { useState, useEffect } from 'react';

export default function Nav() {
  const totalTime = 120;
  // this variable will be updated based on time selected earlier
  // 1 coin will be added every 30s
  const [timeLeft, setTimeLeft] = useState(totalTime);
  const [coins, setCoins] = useState(0);
  // initial usestate coin variable will have to come from backend
  // when the coin is updated it will have to update the backend too

  useEffect(() => {
    if (timeLeft > 0) {
      const timerId = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
        if ((totalTime - timeLeft + 1) % 30 === 0) {
          setCoins(prevCoins => prevCoins + 1);
        }
      }, 1000);
      return () => clearInterval(timerId);
    }
  }, [timeLeft]);

  return (
    <div>
      <nav class="navbar">
        <div class="navbar-left">
            <a class="navbar-brand">Book<span class="brand-color-shift">worm</span></a>
            <a class="nav-link" style={{visibility: "hidden"}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="1.3em" height="1.3em" viewBox="0 -5.5 24 24"><path fill="#47837A" d="M6.75 22q-1.125 0-1.937-.763T4 19.35V5.4q0-.95.588-1.7t1.537-.95l7.5-1.475q.925-.2 1.65.4T16 3.225V15.15q0 .725-.45 1.288t-1.15.687L6.525 18.7q-.225.05-.375.238T6 19.35q0 .275.225.463T6.75 20H18V5q0-.425.288-.712T19 4t.713.288T20 5v15q0 .825-.587 1.413T18 22zm1.45-5.65q.35-.075.575-.35T9 15.375V5.45q0-.475-.363-.775t-.837-.2q-.35.075-.575.35T7 5.45v9.925q0 .475.362.775t.838.2"/></svg>
                Start Reading
            </a>
            <a class="nav-link" style={{visibility: "hidden"}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="1.4em" height="1.4em" viewBox="1 -5.5 24 24"><path fill="#47837A" d="M5 21q-.825 0-1.412-.587T3 19V6.525q0-.35.113-.675t.337-.6L4.7 3.725q.275-.35.687-.538T6.25 3h11.5q.45 0 .863.188t.687.537l1.25 1.525q.225.275.338.6t.112.675V19q0 .825-.587 1.413T19 21zm.4-15h13.2l-.85-1H6.25zM16 8H8v8l4-2l4 2z"/></svg>
                Book Log
            </a>
        </div>
        <div class="navbar-right">
            <span class="coins">
                <svg xmlns="http://www.w3.org/2000/svg" width="1.4em" height="1.4em" viewBox="3 -6 24 24"><path fill="#FFCC4D" d="M17 3.34A10 10 0 1 1 2 12l.005-.324A10 10 0 0 1 17 3.34M12 6a1 1 0 0 0-1 1a3 3 0 1 0 0 6v2a1.02 1.02 0 0 1-.866-.398l-.068-.101a1 1 0 0 0-1.732.998a3 3 0 0 0 2.505 1.5H11a1 1 0 0 0 .883.994L12 18a1 1 0 0 0 1-1l.176-.005A3 3 0 0 0 13 11V9c.358-.012.671.14.866.398l.068.101a1 1 0 0 0 1.732-.998A3 3 0 0 0 13.161 7H13a1 1 0 0 0-1-1m1 7a1 1 0 0 1 0 2zm-2-4v2a1 1 0 0 1 0-2"/></svg>
                {coins}
            </span>
            <button class="home-btn" style={{visibility: "hidden"}}>Shop</button>
        </div>
      </nav>
    </div>
  );
}
