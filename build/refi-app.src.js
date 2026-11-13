
(() => {
  const { useState, useEffect, useRef, useMemo } = React;
  const C = {
    teal: "#28b5cf",
    tealDeep: "#7fd6e6",
    // was deep teal for light card; now light teal readable on dark
    tealText: "#7fd6e6",
    flame: "#F0522B",
    // Text tokens — now light, since text sits on the dark navy card:
    ink: "#FFFFFF",
    // primary text on card (was dark navy)
    ink70: "#C3CBD4",
    // secondary text (was #3a4250)
    slate: "#8f9aa6",
    // muted/caption text (was #5B6570)
    // Card / surface tokens:
    page: "#FFFFFF",
    // page background behind the card
    card: "#0D1424",
    // dark navy card surface
    navy: "#0D1424",
    // explicit deep navy where a dark fill is needed
    cardInset: "#131c2e",
    // slightly lighter navy for inset panels/inputs
    cardLine: "#26303f",
    // hairline borders inside the dark card
    line: "#26303f",
    // legacy alias → dark-card hairline
    surface: "#131c2e",
    // legacy alias → dark-card inset
    white: "#FFFFFF"
  };
  const usd = (n) => isFinite(n) ? "$" + Math.round(n).toLocaleString("en-US") : "$0";
  function payment(principal, annualRate, years) {
    const r = annualRate / 100 / 12;
    const n = years * 12;
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }
  function totalInterest(principal, annualRate, years) {
    return payment(principal, annualRate, years) * years * 12 - principal;
  }
  function useCountUp(target, run, ms = 1100) {
    const [v, setV] = useState(0);
    const raf = useRef();
    useEffect(() => {
      if (!run) return;
      let start;
      const from = 0;
      const step = (t) => {
        if (!start) start = t;
        const p = Math.min((t - start) / ms, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        setV(from + (target - from) * eased);
        if (p < 1) raf.current = requestAnimationFrame(step);
      };
      raf.current = requestAnimationFrame(step);
      return () => cancelAnimationFrame(raf.current);
    }, [target, run, ms]);
    return v;
  }
  function Eyebrow({ children }) {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          fontFamily: "Barlow Condensed, Barlow, sans-serif",
          fontWeight: 600,
          letterSpacing: "0.18em",
          textTransform: "uppercase",
          fontSize: 13,
          color: C.teal,
          marginBottom: 14
        }
      },
      children
    );
  }
  function Question({ children }) {
    return /* @__PURE__ */ React.createElement(
      "h2",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: "clamp(26px, 4.4vw, 38px)",
          lineHeight: 1.12,
          color: C.ink,
          margin: "0 0 8px",
          letterSpacing: "-0.02em"
        }
      },
      children
    );
  }
  function Helper({ children }) {
    return /* @__PURE__ */ React.createElement(
      "p",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontSize: 16,
          lineHeight: 1.5,
          color: C.slate,
          margin: "0 0 30px",
          maxWidth: 460
        }
      },
      children
    );
  }
  function Choice({ label, sub, active, onClick }) {
    const [hover, setHover] = useState(false);
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick,
        onMouseEnter: () => setHover(true),
        onMouseLeave: () => setHover(false),
        style: {
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          width: "100%",
          textAlign: "left",
          padding: "18px 20px",
          marginBottom: 12,
          borderRadius: 14,
          cursor: "pointer",
          border: `1.5px solid ${active ? C.teal : hover ? "#3a4657" : C.line}`,
          background: active ? "rgba(40,181,207,0.10)" : C.cardInset,
          boxShadow: hover && !active ? "0 6px 20px rgba(0,0,0,0.25)" : "none",
          transform: hover ? "translateY(-1px)" : "none",
          transition: "all .16s ease",
          fontFamily: "Barlow, sans-serif"
        }
      },
      /* @__PURE__ */ React.createElement("span", null, /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            display: "block",
            fontWeight: 600,
            fontSize: 18,
            color: C.ink
          }
        },
        label
      ), sub && /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            display: "block",
            fontSize: 14,
            color: C.slate,
            marginTop: 2
          }
        },
        sub
      )),
      /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            width: 22,
            height: 22,
            borderRadius: "50%",
            flexShrink: 0,
            border: `2px solid ${active ? C.teal : "#3a4657"}`,
            background: active ? C.teal : "transparent",
            display: "grid",
            placeItems: "center",
            transition: "all .16s ease"
          }
        },
        active && /* @__PURE__ */ React.createElement(
          "span",
          {
            style: {
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: C.white
            }
          }
        )
      )
    );
  }
  function NumField({ prefix, suffix, value, onChange, placeholder, autoFocus }) {
    const [focus, setFocus] = useState(false);
    const fmt = (raw) => {
      const clean = raw.replace(/[^0-9.]/g, "");
      if (clean === "") return "";
      if (suffix === "%") return clean;
      const num = parseFloat(clean.replace(/,/g, ""));
      if (isNaN(num)) return "";
      return num.toLocaleString("en-US");
    };
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          alignItems: "center",
          gap: 4,
          border: `1.5px solid ${focus ? C.teal : C.line}`,
          borderRadius: 14,
          padding: "16px 18px",
          background: C.cardInset,
          boxShadow: focus ? "0 0 0 4px rgba(40,181,207,0.12)" : "none",
          transition: "all .16s ease",
          marginBottom: 14
        }
      },
      prefix && /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            fontFamily: "Barlow, sans-serif",
            fontSize: 26,
            fontWeight: 500,
            color: C.slate
          }
        },
        prefix
      ),
      /* @__PURE__ */ React.createElement(
        "input",
        {
          className: "moxie-numfield",
          autoFocus,
          inputMode: "decimal",
          value,
          placeholder,
          onFocus: () => setFocus(true),
          onBlur: () => setFocus(false),
          onChange: (e) => onChange(fmt(e.target.value)),
          style: {
            flex: 1,
            border: "none",
            outline: "none",
            background: "transparent",
            fontFamily: "Barlow, sans-serif",
            fontWeight: 600,
            fontSize: 26,
            lineHeight: 1.2,
            color: C.ink,
            width: "100%",
            minWidth: 0,
            letterSpacing: "-0.01em"
          }
        }
      ),
      suffix && /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            fontFamily: "Barlow, sans-serif",
            fontSize: 26,
            fontWeight: 500,
            color: C.slate
          }
        },
        suffix
      )
    );
  }
  function CTA({ children, onClick, disabled, tone = "teal" }) {
    const [hover, setHover] = useState(false);
    const bg = tone === "flame" ? C.flame : C.teal;
    const bgH = tone === "flame" ? "#d84620" : C.tealDeep;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick,
        disabled,
        onMouseEnter: () => setHover(true),
        onMouseLeave: () => setHover(false),
        style: {
          width: "100%",
          padding: "17px 24px",
          borderRadius: 14,
          border: "none",
          cursor: disabled ? "not-allowed" : "pointer",
          background: disabled ? "#2a3547" : hover ? bgH : bg,
          color: C.white,
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 17,
          letterSpacing: "0.01em",
          boxShadow: disabled ? "none" : `0 10px 26px ${tone === "flame" ? "rgba(240,82,43,0.32)" : "rgba(40,181,207,0.32)"}`,
          transform: hover && !disabled ? "translateY(-2px)" : "none",
          transition: "all .18s ease"
        }
      },
      children
    );
  }
  const PHASES = ["Your mortgage", "Your goals", "Your options", "Your results"];
  function ProgressRail({ phase }) {
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, marginBottom: 4 } }, PHASES.map((p, i) => {
      const done = i < phase;
      const now = i === phase;
      return /* @__PURE__ */ React.createElement("div", { key: p, style: { flex: 1, minWidth: 0 } }, /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            height: 4,
            borderRadius: 3,
            background: done || now ? C.teal : "#2a3547",
            opacity: now ? 1 : done ? 0.85 : 1,
            transition: "background .3s ease"
          }
        }
      ), /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            marginTop: 8,
            fontFamily: "Barlow Condensed, Barlow, sans-serif",
            fontWeight: 600,
            fontSize: 12,
            letterSpacing: "0.08em",
            textTransform: "uppercase",
            color: now ? C.ink : C.slate,
            opacity: done || now ? 1 : 0.55,
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis"
          }
        },
        p
      ));
    }));
  }
  function Fade({ k, children }) {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        key: k,
        style: { animation: "moxieIn .34s cubic-bezier(.22,.61,.36,1)" }
      },
      children
    );
  }
  function MoxieRefinance() {
    const [step, setStep] = useState(0);
    const [goal, setGoal] = useState(null);
    const [data, setData] = useState({
      balance: "",
      rate: "",
      years: "24",
      // remaining term default
      home: "",
      cashout: "",
      targetRate: "",
      // rate the client is comparing against (their quote / what-if)
      targetKnown: null,
      // "yes" = they entered a real quoted rate | "explore" = what-if
      // ---- fields the statement parser can fill (all optional, all editable) ----
      lender: "",
      loanType: "",
      // "conventional" | "fha" | "va" | "usda" | "" (unknown)
      hasEscrow: null,
      // true | false | null (unknown) — detected from statement
      escrowMonthly: "",
      // monthly escrow portion, if shown
      propertyAddress: ""
      // captured for the advisor handoff only; never used in math
    });
    const [parse, setParse] = useState({
      status: "idle",
      // idle | reading | review | error
      error: "",
      fields: null,
      // extracted fields awaiting user confirmation
      confidence: null
      // per-field "high" | "low" | null flags
    });
    const [showResults, setShowResults] = useState(false);
    const [lead, setLead] = useState({ name: "", email: "", phone: "", consent: false });
    const [submitted, setSubmitted] = useState(false);
    const [submitState, setSubmitState] = useState({ status: "idle", error: "", leadId: null });
    const statementRef = useRef({ base64: "", name: "", type: "" });
    const set = (k) => (v) => setData((d) => ({ ...d, [k]: v }));
    const num = (s) => parseFloat(String(s).replace(/,/g, "")) || 0;
    const steps = useMemo(() => {
      const base = ["intro", "goal", "upload", "balance", "rate", "home", "compareRate"];
      if (goal === "cash") base.push("cashout");
      base.push("results", "lead");
      return base;
    }, [goal]);
    const cur = steps[step];
    const phaseFor = (name) => {
      if (name === "intro" || name === "upload" || name === "balance" || name === "rate") return 0;
      if (name === "goal") return 1;
      if (name === "home" || name === "cashout" || name === "compareRate") return 2;
      return 3;
    };
    const calc = useMemo(() => {
      const bal = num(data.balance);
      const rate = num(data.rate);
      const yrsLeft = num(data.years) || 24;
      const home = num(data.home) || bal * 1.35;
      if (!bal || !rate) return null;
      const cmp = num(data.targetRate);
      const hasCmp = cmp > 0;
      const newRate30 = cmp;
      const newRate20 = cmp;
      const curPay = payment(bal, rate, yrsLeft);
      const pay30 = hasCmp ? payment(bal, newRate30, 30) : null;
      const pay20 = hasCmp ? payment(bal, newRate20, 20) : null;
      const ltv = home > 0 ? bal / home : 1;
      const monthlySave = hasCmp ? curPay - pay30 : 0;
      const lenderFees = bal * 9e-3;
      const thirdPartyFlat = 1300;
      const baseCosts = lenderFees + thirdPartyFlat;
      const conventional = data.loanType === "conventional" || data.loanType === "";
      const eligibleToWaive = conventional && ltv <= 0.8;
      const escrowsRequired = data.hasEscrow === true || !eligibleToWaive;
      const escrowMo = num(data.escrowMonthly) || home * 0.0125 / 12;
      const escrowFunding = escrowsRequired ? escrowMo * 2 : 0;
      const costs = Math.round(baseCosts + escrowFunding);
      const escrowWaived = !escrowsRequired;
      const breakEven = hasCmp && monthlySave > 0 ? Math.ceil(costs / monthlySave) : Infinity;
      const maxCash = Math.max(home * 0.8 - bal, 0);
      const cashAsk = Math.min(num(data.cashout) || maxCash, maxCash);
      const cashLoan = bal + cashAsk;
      const cashPay = hasCmp ? payment(cashLoan, newRate30, 30) : null;
      const interestStay = totalInterest(bal, rate, yrsLeft);
      const interest20 = hasCmp ? totalInterest(bal, newRate20, 20) : null;
      const interestSaved = hasCmp ? interestStay - interest20 : 0;
      let rec = "lower";
      if (goal === "cash" && maxCash > 5e3) rec = "cash";
      else if (goal === "faster" && interestSaved > 0) rec = "faster";
      else if (!hasCmp) rec = "quote";
      else if (monthlySave < 40 || breakEven > 60) rec = "quote";
      else rec = "lower";
      return {
        bal,
        rate,
        yrsLeft,
        home,
        ltv,
        cmp,
        hasCmp,
        curPay,
        pay30,
        pay20,
        cashPay,
        newRate30,
        newRate20,
        monthlySave,
        costs,
        breakEven,
        escrowWaived,
        escrowsRequired,
        eligibleToWaive,
        maxCash,
        cashAsk,
        cashLoan,
        interestSaved,
        rec
      };
    }, [data, goal]);
    const next = () => setStep((s) => Math.min(s + 1, steps.length - 1));
    const back = () => setStep((s) => Math.max(s - 1, 0));
    const USE_BACKEND = false;
    const MOXIE_PARSE_ENDPOINT = "/api/parse-statement";
    const fileToBase64 = (file) => new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = () => res(String(r.result).split(",")[1]);
      r.onerror = () => rej(new Error("Could not read that file."));
      r.readAsDataURL(file);
    });
    async function parseViaMoxieBackend(file) {
      const form = new FormData();
      form.append("statement", file);
      const resp = await fetch(MOXIE_PARSE_ENDPOINT, { method: "POST", body: form });
      if (!resp.ok) throw new Error("Parsing service unavailable.");
      return await resp.json();
    }
    async function parseViaAnthropic(file) {
      const b64 = await fileToBase64(file);
      const isPdf = file.type === "application/pdf";
      const mediaType = isPdf ? "application/pdf" : file.type || "image/jpeg";
      const block = isPdf ? { type: "document", source: { type: "base64", media_type: mediaType, data: b64 } } : { type: "image", source: { type: "base64", media_type: mediaType, data: b64 } };
      const instruction = `You are reading a mortgage statement. Extract ONLY these fields and return strict JSON, no prose, no markdown. Do NOT extract account numbers, SSNs, or any identifier we didn't ask for. Fields: {"lender": string|null, "balance": number|null (current principal balance / unpaid principal), "rate": number|null (note/interest rate as a percent, e.g. 6.875), "loanType": one of "conventional","fha","va","usda",null, "hasEscrow": boolean|null (true if the statement shows an escrow/impound balance or an escrow portion of the payment), "escrowMonthly": number|null (the monthly escrow portion of the payment if shown), "propertyAddress": string|null (the mortgaged property address), "homeValue": number|null (only if an appraised/estimated value appears; otherwise null)}. If a field is not clearly present, use null. ALSO include a "confidence" object mapping each field name above to "high", "low", or null (null when the field itself is null). Use "high" only when the value is clearly and unambiguously printed on the statement; use "low" when you inferred it, it was hard to read, or you're unsure. loanType is often not stated explicitly \u2014 mark it "low" unless the statement names the program. Return JSON only.`;
      const resp = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-6",
          max_tokens: 1e3,
          messages: [{ role: "user", content: [block, { type: "text", text: instruction }] }]
        })
      });
      if (!resp.ok) throw new Error("Couldn't read that statement. Try a clearer photo or PDF.");
      const dj = await resp.json();
      const text = (dj.content || []).map((c) => c.type === "text" ? c.text : "").join("").replace(/```json|```/g, "").trim();
      return JSON.parse(text);
    }
    async function handleStatement(file) {
      if (!file) return;
      const okType = /pdf|image\//.test(file.type);
      if (!okType) {
        setParse({ status: "error", error: "Please upload a PDF or photo of your statement.", fields: null });
        return;
      }
      if (file.size > 12 * 1024 * 1024) {
        setParse({ status: "error", error: "That file is a bit large \u2014 please keep it under 12 MB.", fields: null });
        return;
      }
      setParse({ status: "reading", error: "", fields: null });
      try {
        try {
          const b64 = await fileToBase64(file);
          statementRef.current = { base64: b64, name: file.name || "statement", type: file.type || "" };
        } catch (_) {
        }
        const raw = USE_BACKEND ? await parseViaMoxieBackend(file) : await parseViaAnthropic(file);
        const fields = {
          lender: raw.lender || "",
          balance: raw.balance != null ? Math.round(raw.balance).toLocaleString("en-US") : "",
          rate: raw.rate != null ? String(raw.rate) : "",
          loanType: raw.loanType || "",
          hasEscrow: typeof raw.hasEscrow === "boolean" ? raw.hasEscrow : null,
          escrowMonthly: raw.escrowMonthly != null ? String(Math.round(raw.escrowMonthly)) : "",
          propertyAddress: raw.propertyAddress || "",
          home: raw.homeValue != null ? Math.round(raw.homeValue).toLocaleString("en-US") : ""
        };
        const rawConf = raw.confidence || {};
        const conf = {
          lender: fields.lender ? rawConf.lender || "low" : null,
          balance: fields.balance ? rawConf.balance || "low" : null,
          rate: fields.rate ? rawConf.rate || "low" : null,
          loanType: fields.loanType ? rawConf.loanType || "low" : null,
          hasEscrow: fields.hasEscrow != null ? rawConf.hasEscrow || "low" : null,
          escrowMonthly: fields.escrowMonthly ? rawConf.escrowMonthly || "low" : null,
          propertyAddress: fields.propertyAddress ? rawConf.propertyAddress || "low" : null,
          home: fields.home ? rawConf.homeValue || "low" : null
        };
        setParse({ status: "review", error: "", fields, confidence: conf });
      } catch (e) {
        setParse({ status: "error", error: e.message || "Something went wrong reading that file.", fields: null });
      }
    }
    function applyParsed(fields) {
      setData((d) => ({
        ...d,
        balance: fields.balance || d.balance,
        rate: fields.rate || d.rate,
        home: fields.home || d.home,
        lender: fields.lender || d.lender,
        loanType: fields.loanType || d.loanType,
        hasEscrow: fields.hasEscrow,
        escrowMonthly: fields.escrowMonthly || d.escrowMonthly,
        propertyAddress: fields.propertyAddress || d.propertyAddress
      }));
      setParse((p) => ({ ...p, status: "idle" }));
      const haveBal = !!fields.balance;
      const haveRate = !!fields.rate;
      const haveHome = !!fields.home;
      const target = !haveBal ? "balance" : !haveRate ? "rate" : !haveHome ? "home" : "compareRate";
      setStep(steps.indexOf(target));
    }
    const LEAD_ENDPOINT = "https://script.google.com/macros/s/AKfycby2DNAgTJREXdoEPWPobju74TheeTS5ne4LdXR16cVG9jW7HfcwCJchxGgthsM47Ndj/exec";
    const SHARED_SECRET = "joasidfjoaiewlkejwlkessddfsqwe";
    function buildLeadPayload() {
      const c = calc || {};
      const goalLabel = {
        lower: "Lower my payment",
        cash: "Get cash from equity",
        faster: "Pay off faster",
        unsure: "Not sure yet"
      }[goal] || "Not specified";
      const fields = {
        "Goal": goalLabel,
        "Mortgage Balance": data.balance ? "$" + data.balance : "",
        "Current Rate": data.rate ? data.rate + "%" : "",
        "Home Value": data.home ? "$" + data.home : "",
        "Comparison Rate": data.targetRate ? data.targetRate + "%" : "",
        "Rate Source": data.targetKnown === "yes" ? "Quoted" : data.targetKnown === "explore" ? "Exploring" : "",
        "Lender": data.lender || "",
        "Loan Type": data.loanType || "",
        "Escrow Account": data.hasEscrow === true ? "Yes" : data.hasEscrow === false ? "No" : "",
        "Cash Out Requested": data.cashout ? "$" + data.cashout : "",
        "Statement Uploaded": statementRef.current.base64 ? "Yes (" + statementRef.current.name + ")" : "No"
      };
      const results = {};
      if (c.hasCmp) {
        results["Current Payment"] = usd(c.curPay);
        results["New Payment"] = usd(c.pay30);
        results["Monthly Change"] = c.monthlySave >= 0 ? "-" + usd(c.monthlySave) + "/mo" : "+" + usd(Math.abs(c.monthlySave)) + "/mo";
        if (c.monthlySave > 0) results["Annual Savings"] = usd(c.monthlySave * 12);
        results["Est. Costs"] = usd(c.costs);
        results["Break-even"] = isFinite(c.breakEven) ? c.breakEven + " months" : "n/a";
        if (c.maxCash > 0) results["Max Cash-Out"] = usd(c.maxCash);
        results["Recommended"] = {
          lower: "Lower payment",
          cash: "Cash out",
          faster: "Faster payoff",
          quote: "Get a real rate"
        }[c.rec] || "";
      }
      const clean = (o) => Object.fromEntries(Object.entries(o).filter(([, v]) => v !== "" && v != null));
      const payload = {
        name: lead.name,
        email: lead.email,
        phone: lead.phone,
        consent: lead.consent === true,
        cta: "Refinance Review",
        // → tag "CTA: Refinance Review"
        source: "MoxieMortgage.com \u2014 Refinance Review",
        pageUrl: typeof window !== "undefined" && window.location && window.location.href || "",
        submittedAt: (/* @__PURE__ */ new Date()).toISOString(),
        fields: clean(fields),
        results: clean(results)
      };
      if (data.propertyAddress) payload.streetAddress = data.propertyAddress;
      if (SHARED_SECRET) payload.secret = SHARED_SECRET;
      if (statementRef.current.base64) {
        payload.statement = {
          base64: statementRef.current.base64,
          filename: statementRef.current.name,
          mimeType: statementRef.current.type
        };
      }
      return payload;
    }
    async function submitLead() {
      if (!lead.name || !lead.email || !lead.consent) return;
      setSubmitState({ status: "sending", error: "", leadId: null });
      const payload = buildLeadPayload();
      const form = new URLSearchParams();
      form.append("payload", JSON.stringify(payload));
      try {
        const resp = await fetch(LEAD_ENDPOINT, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8" },
          body: form.toString(),
          redirect: "follow"
        });
        const out = await resp.json().catch(() => null);
        if (out && out.ok) {
          setSubmitState({ status: "done", error: "", leadId: out.leadId || out.lofty && out.lofty.leadId || null });
          setSubmitted(true);
        } else if (out && out.ok === false) {
          throw new Error(out.error || "Submission was rejected.");
        } else {
          await fetch(LEAD_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8" },
            body: form.toString(),
            mode: "no-cors"
          });
          setSubmitState({ status: "done", error: "", leadId: null });
          setSubmitted(true);
        }
      } catch (e) {
        setSubmitState({ status: "error", error: e.message || "Submission failed.", leadId: null });
        setSubmitted(true);
      }
    }
    const canAdvance = () => {
      if (cur === "goal") return !!goal;
      if (cur === "balance") return num(data.balance) > 0;
      if (cur === "rate") return num(data.rate) > 0;
      if (cur === "home") return num(data.home) > 0;
      if (cur === "compareRate") return num(data.targetRate) > 0;
      return true;
    };
    useEffect(() => {
      if (cur === "results") {
        setShowResults(false);
        const t = setTimeout(() => setShowResults(true), 120);
        return () => clearTimeout(t);
      }
    }, [cur]);
    const goalHeadline = {
      lower: "lower your payment",
      cash: "tap your equity",
      faster: "pay it off sooner",
      unsure: "find your best move"
    };
    const goalNext = {
      lower: "See how much I could save",
      cash: "See how much cash I could get",
      faster: "See my options to shorten loan",
      unsure: "See my best options"
    }[goal] || "See my results";
    const compareRateNext = goal === "cash" ? "Continue" : goalNext;
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          minHeight: "100vh",
          width: "100%",
          fontFamily: "Barlow, sans-serif",
          background: C.page,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "clamp(12px, 3vw, 40px)",
          boxSizing: "border-box",
          position: "relative"
        }
      },
      /* @__PURE__ */ React.createElement(StyleTag, null),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            width: "100%",
            maxWidth: cur === "results" ? 1020 : 740,
            transition: "max-width .3s ease",
            position: "relative",
            zIndex: 1
          }
        },
        /* @__PURE__ */ React.createElement(
          "div",
          {
            style: {
              display: "flex",
              alignItems: "center",
              marginBottom: 16
            }
          },
          /* @__PURE__ */ React.createElement(
            "img",
            {
              src: MOXIE_LOGO_DARK,
              alt: "Moxie Mortgage",
              style: { height: 20, width: "auto", display: "block" }
            }
          )
        ),
        /* @__PURE__ */ React.createElement(
          "div",
          {
            style: {
              background: C.card,
              borderRadius: 22,
              padding: "clamp(40px, 5vw, 64px) clamp(24px, 3.4vw, 44px)",
              boxShadow: "0 24px 70px rgba(13,20,36,0.28)",
              position: "relative",
              overflow: "hidden"
            }
          },
          /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                position: "absolute",
                width: 460,
                height: 460,
                borderRadius: "50%",
                background: "radial-gradient(circle, rgba(40,181,207,0.20) 0%, transparent 70%)",
                top: -180,
                right: -140,
                pointerEvents: "none",
                zIndex: 0
              }
            }
          ),
          /* @__PURE__ */ React.createElement("div", { style: { position: "relative", zIndex: 1 } }, cur !== "intro" && cur !== "lead" && /* @__PURE__ */ React.createElement("div", { style: { marginBottom: 30 } }, /* @__PURE__ */ React.createElement(ProgressRail, { phase: phaseFor(cur) })), cur === "intro" && /* @__PURE__ */ React.createElement(Fade, { k: "intro" }, /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                fontFamily: "Barlow Condensed, Barlow, sans-serif",
                fontWeight: 700,
                letterSpacing: "0.18em",
                textTransform: "uppercase",
                fontSize: 13,
                color: C.teal,
                marginBottom: 22
              }
            },
            "Your new payment in 60 seconds"
          ), /* @__PURE__ */ React.createElement(
            "h1",
            {
              style: {
                fontFamily: "Barlow, sans-serif",
                fontWeight: 700,
                fontSize: "clamp(30px, 5.2vw, 50px)",
                lineHeight: 1.06,
                letterSpacing: "-0.03em",
                color: C.ink,
                margin: "0 0 26px",
                textWrap: "balance",
                maxWidth: 460
              }
            },
            "How much could you be saving on your mortgage?"
          ), /* @__PURE__ */ React.createElement(
            "p",
            {
              style: {
                fontFamily: "Barlow, sans-serif",
                fontSize: 16,
                lineHeight: 1.5,
                color: C.slate,
                margin: "0 0 34px",
                maxWidth: 460
              }
            },
            "Answer a few quick questions and we\u2019ll show you, in plain numbers, what your payment could look like. No guesswork and no credit check."
          ), /* @__PURE__ */ React.createElement(CTA, { onClick: next }, "Show me my numbers"), /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                display: "flex",
                flexWrap: "wrap",
                justifyContent: "center",
                gap: 8,
                marginTop: 18
              }
            },
            ["60 seconds", "No credit check"].map((t) => /* @__PURE__ */ React.createElement(
              "span",
              {
                key: t,
                style: {
                  display: "inline-flex",
                  alignItems: "center",
                  gap: 6,
                  fontFamily: "Barlow, sans-serif",
                  fontWeight: 600,
                  fontSize: 12.5,
                  color: C.tealDeep,
                  background: "rgba(40,181,207,0.10)",
                  border: "1px solid rgba(40,181,207,0.28)",
                  borderRadius: 20,
                  padding: "6px 12px",
                  whiteSpace: "nowrap"
                }
              },
              /* @__PURE__ */ React.createElement("svg", { width: "12", height: "12", viewBox: "0 0 24 24", fill: "none", style: { flexShrink: 0 } }, /* @__PURE__ */ React.createElement("path", { d: "M5 13l4 4L19 7", stroke: C.teal, strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" })),
              t
            ))
          )), cur === "goal" && /* @__PURE__ */ React.createElement(Fade, { k: "goal" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your goals"), /* @__PURE__ */ React.createElement(Question, null, "What would you like your mortgage to do for you?"), /* @__PURE__ */ React.createElement(Helper, null, "Pick the one that matters most right now. We\u2019ll tailor everything after this to match."), /* @__PURE__ */ React.createElement(Choice, { label: "Lower my monthly payment", sub: "Put a few hundred back in your pocket", active: goal === "lower", onClick: () => setGoal("lower") }), /* @__PURE__ */ React.createElement(Choice, { label: "Get cash from my equity", sub: "For renovations, debt, or big plans", active: goal === "cash", onClick: () => setGoal("cash") }), /* @__PURE__ */ React.createElement(Choice, { label: "Pay off my mortgage faster", sub: "Own it years sooner, skip interest", active: goal === "faster", onClick: () => setGoal("faster") }), /* @__PURE__ */ React.createElement(Choice, { label: "I'm not sure yet", sub: "Show me what makes the most sense", active: goal === "unsure", onClick: () => setGoal("unsure") }), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 24 } }, /* @__PURE__ */ React.createElement(CTA, { onClick: next, disabled: !canAdvance() }, "Continue"))), cur === "upload" && /* @__PURE__ */ React.createElement(Fade, { k: "upload" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Optional shortcut"), parse.status === "review" && parse.fields ? /* @__PURE__ */ React.createElement(
            ParsedReview,
            {
              fields: parse.fields,
              confidence: parse.confidence || {},
              onEdit: (k, v) => setParse((p) => ({
                ...p,
                fields: { ...p.fields, [k]: v },
                // editing a field counts as the user verifying it → clear its flag
                confidence: { ...p.confidence || {}, [k]: p.confidence && p.confidence[k] === "low" ? "high" : (p.confidence || {})[k] }
              })),
              onConfirm: () => applyParsed(parse.fields),
              onDiscard: () => setParse({ status: "idle", error: "", fields: null, confidence: null }),
              usd
            }
          ) : /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Question, null, "Have your statement handy? Skip the typing."), /* @__PURE__ */ React.createElement(Helper, null, "Upload a recent mortgage statement and we\u2019ll read the details for you \u2014 balance, rate, lender, and escrow \u2014 so you don\u2019t have to enter them. You\u2019ll get to review everything before we use it."), parse.status === "reading" ? /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                display: "flex",
                alignItems: "center",
                gap: 14,
                padding: "22px 20px",
                borderRadius: 14,
                border: `1.5px solid ${C.line}`,
                background: C.surface,
                marginBottom: 18
              }
            },
            /* @__PURE__ */ React.createElement(Spinner, null),
            /* @__PURE__ */ React.createElement("div", { style: { fontFamily: "Barlow, sans-serif" } }, /* @__PURE__ */ React.createElement("div", { style: { fontWeight: 600, color: C.ink } }, "Reading your statement\u2026"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.5, color: C.slate } }, "This usually takes a few seconds."))
          ) : /* @__PURE__ */ React.createElement(UploadDrop, { onFile: handleStatement }), parse.status === "error" && /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                fontSize: 14,
                color: C.flame,
                fontWeight: 500,
                margin: "0 0 16px"
              }
            },
            parse.error
          ), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 12 } }, /* @__PURE__ */ React.createElement(
            "button",
            {
              onClick: back,
              style: {
                padding: "17px 22px",
                borderRadius: 14,
                border: `1.5px solid ${C.line}`,
                background: C.cardInset,
                color: C.slate,
                fontFamily: "Barlow, sans-serif",
                fontWeight: 600,
                fontSize: 16,
                cursor: "pointer"
              }
            },
            "Back"
          ), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement(CTA, { onClick: next }, "I\u2019ll type it in instead"))))), cur === "balance" && /* @__PURE__ */ React.createElement(Fade, { k: "balance" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your mortgage"), /* @__PURE__ */ React.createElement(Question, null, "About how much do you still owe?"), /* @__PURE__ */ React.createElement(Helper, null, "A rough number is fine \u2014 we just need a starting point."), /* @__PURE__ */ React.createElement(NumField, { prefix: "$", value: data.balance, onChange: set("balance"), placeholder: "482,000", autoFocus: true }), num(data.balance) > 0 && /* @__PURE__ */ React.createElement("p", { style: { fontSize: 15, color: C.tealDeep, fontWeight: 500, margin: "2px 0 26px" } }, "Perfect \u2014 that\u2019s all we need to start the math."), /* @__PURE__ */ React.createElement(NavRow, { onBack: back, onNext: next, disabled: !canAdvance() })), cur === "rate" && /* @__PURE__ */ React.createElement(Fade, { k: "rate" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your mortgage"), /* @__PURE__ */ React.createElement(Question, null, "What\u2019s your current interest rate?"), /* @__PURE__ */ React.createElement(Helper, null, "You\u2019ll find this on your monthly statement or closing paperwork."), /* @__PURE__ */ React.createElement(NumField, { suffix: "%", value: data.rate, onChange: set("rate"), placeholder: "6.875", autoFocus: true }), num(data.rate) > 0 && /* @__PURE__ */ React.createElement("p", { style: { fontSize: 15, color: C.tealDeep, fontWeight: 500, margin: "2px 0 26px" } }, "Good \u2014 now let\u2019s see how much lower it could go."), /* @__PURE__ */ React.createElement(NavRow, { onBack: back, onNext: next, disabled: !canAdvance() })), cur === "home" && /* @__PURE__ */ React.createElement(Fade, { k: "home" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your options"), /* @__PURE__ */ React.createElement(Question, null, "What\u2019s your home worth today?"), /* @__PURE__ */ React.createElement(Helper, null, "Your best estimate is plenty. This helps us see how much equity you\u2019re working with."), /* @__PURE__ */ React.createElement(NumField, { prefix: "$", value: data.home, onChange: set("home"), placeholder: "720,000", autoFocus: true }), calc && num(data.home) > 0 && /* @__PURE__ */ React.createElement("p", { style: { fontSize: 15, color: C.tealDeep, fontWeight: 500, margin: "2px 0 26px" } }, "That\u2019s roughly ", Math.round((1 - calc.ltv) * 100), "% equity in your home."), /* @__PURE__ */ React.createElement(NavRow, { onBack: back, onNext: next, disabled: !canAdvance(), nextLabel: "Continue" })), cur === "compareRate" && /* @__PURE__ */ React.createElement(Fade, { k: "compareRate" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your options"), !data.targetKnown ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Question, null, "Do you already have a rate in mind?"), /* @__PURE__ */ React.createElement(Helper, null, "To show you a real comparison, we use a rate ", /* @__PURE__ */ React.createElement("em", null, "you"), " give us \u2014 never one we make up. Have you been quoted a rate, or are you just exploring what\u2019s possible?"), /* @__PURE__ */ React.createElement(
            Choice,
            {
              label: "I have a quoted rate",
              sub: "Compare against a real number I've been given",
              active: data.targetKnown === "yes",
              onClick: () => setData((d) => ({ ...d, targetKnown: "yes", targetRate: "" }))
            }
          ), /* @__PURE__ */ React.createElement(
            Choice,
            {
              label: "I'm just exploring",
              sub: "Show me what different rates would look like",
              active: data.targetKnown === "explore",
              onClick: () => setData((d) => ({ ...d, targetKnown: "explore", targetRate: "" }))
            }
          ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 24 } }, /* @__PURE__ */ React.createElement(
            "button",
            {
              onClick: back,
              style: {
                padding: "17px 22px",
                borderRadius: 14,
                border: `1.5px solid ${C.line}`,
                background: C.cardInset,
                color: C.slate,
                fontFamily: "Barlow, sans-serif",
                fontWeight: 600,
                fontSize: 16,
                cursor: "pointer"
              }
            },
            "Back"
          ))) : data.targetKnown === "yes" ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Question, null, "What rate were you quoted?"), /* @__PURE__ */ React.createElement(Helper, null, "Enter the rate exactly as you were quoted it. We\u2019ll build your comparison on that number and nothing else."), /* @__PURE__ */ React.createElement(NumField, { suffix: "%", value: data.targetRate, onChange: set("targetRate"), placeholder: "6.000", autoFocus: true }), num(data.targetRate) > 0 && num(data.rate) > 0 && /* @__PURE__ */ React.createElement("p", { style: { fontSize: 15, color: C.tealDeep, fontWeight: 500, margin: "2px 0 8px" } }, num(data.targetRate) < num(data.rate) ? `That's ${(num(data.rate) - num(data.targetRate)).toFixed(3)} points below your current rate.` : num(data.targetRate) > num(data.rate) ? `That's above your current rate \u2014 we'll show you what that looks like too.` : `That matches your current rate.`), /* @__PURE__ */ React.createElement(
            "div",
            {
              style: {
                fontSize: 13.5,
                lineHeight: 1.5,
                color: C.slate,
                background: C.surface,
                border: `1px solid ${C.line}`,
                borderRadius: 12,
                padding: "12px 14px",
                margin: "8px 0 24px"
              }
            },
            "We\u2019ll calculate your payment at exactly this rate \u2014 no assumptions added."
          ), /* @__PURE__ */ React.createElement(
            NavRow,
            {
              onBack: () => setData((d) => ({ ...d, targetKnown: null, targetRate: "" })),
              onNext: next,
              disabled: !canAdvance(),
              nextLabel: compareRateNext
            }
          )) : /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Question, null, "What rate would you like to explore?"), /* @__PURE__ */ React.createElement(Helper, null, "Pick any rate you\u2019re curious about and we\u2019ll show you what that payment would look like. It\u2019s a what-if, not an offer \u2014 a great way to see what\u2019s worth chasing."), /* @__PURE__ */ React.createElement(NumField, { suffix: "%", value: data.targetRate, onChange: set("targetRate"), placeholder: "6.000", autoFocus: true }), num(data.targetRate) > 0 && num(data.rate) > 0 && /* @__PURE__ */ React.createElement("p", { style: { fontSize: 15, color: C.tealDeep, fontWeight: 500, margin: "2px 0 8px" } }, num(data.targetRate) < num(data.rate) ? `That's ${(num(data.rate) - num(data.targetRate)).toFixed(3)} points below your current rate \u2014 let's see the impact.` : num(data.targetRate) > num(data.rate) ? `That's above your current rate \u2014 we'll show you what that looks like too.` : `That matches your current rate.`), /* @__PURE__ */ React.createElement("div", { style: { marginBottom: 24 } }), /* @__PURE__ */ React.createElement(
            NavRow,
            {
              onBack: () => setData((d) => ({ ...d, targetKnown: null, targetRate: "" })),
              onNext: next,
              disabled: !canAdvance(),
              nextLabel: compareRateNext
            }
          ))), cur === "cashout" && /* @__PURE__ */ React.createElement(Fade, { k: "cashout" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your options"), /* @__PURE__ */ React.createElement(Question, null, "How much cash are you hoping to take out?"), /* @__PURE__ */ React.createElement(Helper, null, "Based on your equity, you could access up to about", " ", /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, usd(calc?.maxCash || 0)), ". Leave it blank to see the maximum."), /* @__PURE__ */ React.createElement(NumField, { prefix: "$", value: data.cashout, onChange: set("cashout"), placeholder: String(Math.round(calc?.maxCash || 0)), autoFocus: true }), /* @__PURE__ */ React.createElement(NavRow, { onBack: back, onNext: next, disabled: false, nextLabel: "See how much cash I could get" })), cur === "results" && calc && /* @__PURE__ */ React.createElement(Results, { calc, goal, show: showResults, onBack: back, onNext: next, usd }), cur === "lead" && (() => {
            const leadCopy = {
              lower: {
                eyebrow: "Lock in a lower payment",
                headline: "Ready to turn this into a real lower payment?",
                cta: "Get my lower-payment options"
              },
              cash: {
                eyebrow: "Put your equity to work",
                headline: "Ready to see the real cash you could pull out?",
                cta: "Get my cash-out options"
              },
              faster: {
                eyebrow: "A shorter road to payoff",
                headline: "Ready to map out your fastest path to mortgage-free?",
                cta: "Get my payoff options"
              },
              unsure: {
                eyebrow: "Your clearest next step",
                headline: "Ready to see which option actually fits you best?",
                cta: "Get my personalized options"
              }
            };
            const lc = leadCopy[goal] || leadCopy.unsure;
            return /* @__PURE__ */ React.createElement(Fade, { k: "lead" }, !submitted ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Eyebrow, null, lc.eyebrow), /* @__PURE__ */ React.createElement(Question, null, lc.headline), /* @__PURE__ */ React.createElement(Helper, null, "These numbers are your estimate. A Moxie advisor can pull real loan options for your exact situation, then tell you straight whether refinancing is worth it. They only reach out when you\u2019re ready."), /* @__PURE__ */ React.createElement(LeadField, { label: "Your name", value: lead.name, onChange: (v) => setLead((l) => ({ ...l, name: v })), placeholder: "Jordan Rivera" }), /* @__PURE__ */ React.createElement(LeadField, { label: "Email", value: lead.email, onChange: (v) => setLead((l) => ({ ...l, email: v })), placeholder: "jordan@email.com", type: "email" }), /* @__PURE__ */ React.createElement(LeadField, { label: "Phone", value: lead.phone, onChange: (v) => setLead((l) => ({ ...l, phone: v })), placeholder: "(555) 012-3456", type: "tel" }), /* @__PURE__ */ React.createElement(
              ConsentCheck,
              {
                checked: lead.consent,
                onToggle: () => setLead((l) => ({ ...l, consent: !l.consent }))
              }
            ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 18 } }, /* @__PURE__ */ React.createElement(
              CTA,
              {
                tone: "flame",
                onClick: submitLead,
                disabled: !lead.name || !lead.email || !lead.consent || submitState.status === "sending"
              },
              submitState.status === "sending" ? "Sending\u2026" : lc.cta
            )), /* @__PURE__ */ React.createElement("p", { style: { textAlign: "center", fontSize: 13, color: C.slate, marginTop: 14, marginBottom: 0 } }, "No credit impact \xB7 No obligation \xB7 Your info stays private")) : /* @__PURE__ */ React.createElement("div", { style: { textAlign: "center", padding: "20px 0" } }, /* @__PURE__ */ React.createElement(
              "div",
              {
                style: {
                  width: 64,
                  height: 64,
                  borderRadius: "50%",
                  background: "rgba(40,181,207,0.12)",
                  display: "grid",
                  placeItems: "center",
                  margin: "0 auto 20px",
                  animation: "moxiePop .5s cubic-bezier(.22,.61,.36,1)"
                }
              },
              /* @__PURE__ */ React.createElement("svg", { width: "30", height: "30", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React.createElement("path", { d: "M5 13l4 4L19 7", stroke: C.teal, strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }))
            ), /* @__PURE__ */ React.createElement(Question, null, "You\u2019re all set, ", lead.name.split(" ")[0] || "there", "."), /* @__PURE__ */ React.createElement(Helper, null, "A Moxie advisor will reach out with real, personalized options based on the numbers you shared. Keep an eye on your inbox at ", lead.email, "."), submitState.status === "error" && /* @__PURE__ */ React.createElement(
              "div",
              {
                style: {
                  fontSize: 13,
                  color: C.slate,
                  background: C.surface,
                  border: `1px solid ${C.line}`,
                  borderRadius: 12,
                  padding: "12px 14px",
                  marginTop: 8,
                  textAlign: "left",
                  lineHeight: 1.5,
                  maxWidth: 460,
                  marginLeft: "auto",
                  marginRight: "auto"
                }
              },
              "We saved your details, but there was a hiccup sending them through just now. No need to re-enter anything \u2014 a Moxie advisor will still follow up."
            )));
          })())
        ),
        /* @__PURE__ */ React.createElement(
          "p",
          {
            style: {
              fontSize: 12,
              color: C.slate,
              textAlign: "center",
              marginTop: 18,
              maxWidth: 560,
              marginLeft: "auto",
              marginRight: "auto",
              lineHeight: 1.5
            }
          },
          "Estimates are illustrative and not a loan offer, commitment, or underwriting decision. Actual rates, costs, and terms depend on credit, property, and market conditions."
        )
      )
    );
  }
  function NavRow({ onBack, onNext, disabled, nextLabel = "Continue" }) {
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 12, alignItems: "center" } }, /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onBack,
        style: {
          padding: "17px 22px",
          borderRadius: 14,
          border: `1.5px solid ${C.line}`,
          background: C.cardInset,
          color: C.slate,
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 16,
          cursor: "pointer"
        }
      },
      "Back"
    ), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement(CTA, { onClick: onNext, disabled }, nextLabel)));
  }
  function LeadField({ label, value, onChange, placeholder, type = "text" }) {
    const [focus, setFocus] = useState(false);
    return /* @__PURE__ */ React.createElement("div", { style: { marginBottom: 14 } }, /* @__PURE__ */ React.createElement(
      "label",
      {
        style: {
          display: "block",
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 13,
          color: C.ink70,
          marginBottom: 6,
          letterSpacing: "0.02em"
        }
      },
      label
    ), /* @__PURE__ */ React.createElement(
      "input",
      {
        type,
        value,
        placeholder,
        onFocus: () => setFocus(true),
        onBlur: () => setFocus(false),
        onChange: (e) => onChange(e.target.value),
        style: {
          width: "100%",
          boxSizing: "border-box",
          padding: "15px 16px",
          borderRadius: 12,
          border: `1.5px solid ${focus ? C.teal : C.line}`,
          boxShadow: focus ? "0 0 0 4px rgba(40,181,207,0.12)" : "none",
          outline: "none",
          fontFamily: "Barlow, sans-serif",
          fontSize: 17,
          color: C.ink,
          transition: "all .16s ease"
        }
      }
    ));
  }
  function ConsentCheck({ checked, onToggle }) {
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onToggle,
        style: {
          display: "flex",
          alignItems: "flex-start",
          gap: 12,
          width: "100%",
          textAlign: "left",
          marginTop: 16,
          padding: "12px 4px 0",
          background: "transparent",
          border: "none",
          cursor: "pointer"
        }
      },
      /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            width: 22,
            height: 22,
            borderRadius: 6,
            flexShrink: 0,
            marginTop: 1,
            border: `1.5px solid ${checked ? C.teal : "#3a4657"}`,
            background: checked ? C.teal : C.cardInset,
            display: "grid",
            placeItems: "center",
            transition: "all .16s ease"
          }
        },
        checked && /* @__PURE__ */ React.createElement("svg", { width: "14", height: "14", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React.createElement("path", { d: "M5 13l4 4L19 7", stroke: C.white, strokeWidth: "3", strokeLinecap: "round", strokeLinejoin: "round" }))
      ),
      /* @__PURE__ */ React.createElement("span", { style: { fontFamily: "Barlow, sans-serif", fontSize: 13, lineHeight: 1.5, color: C.slate } }, "I\u2019d like a Moxie advisor to contact me about my refinance options by phone, text, or email. I understand this is about my request and isn\u2019t a condition of any purchase.")
    );
  }
  function Spinner() {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          width: 26,
          height: 26,
          borderRadius: "50%",
          border: `3px solid ${C.line}`,
          borderTopColor: C.teal,
          animation: "moxieSpin .8s linear infinite",
          flexShrink: 0
        }
      }
    );
  }
  function UploadDrop({ onFile }) {
    const inputRef = useRef();
    const [drag, setDrag] = useState(false);
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(
      "input",
      {
        ref: inputRef,
        type: "file",
        accept: "application/pdf,image/*",
        style: { display: "none" },
        onChange: (e) => onFile(e.target.files && e.target.files[0])
      }
    ), /* @__PURE__ */ React.createElement(
      "div",
      {
        onClick: () => inputRef.current && inputRef.current.click(),
        onDragOver: (e) => {
          e.preventDefault();
          setDrag(true);
        },
        onDragLeave: () => setDrag(false),
        onDrop: (e) => {
          e.preventDefault();
          setDrag(false);
          onFile(e.dataTransfer.files && e.dataTransfer.files[0]);
        },
        style: {
          border: `2px dashed ${drag ? C.teal : "#3a4657"}`,
          background: drag ? "rgba(40,181,207,0.06)" : C.surface,
          borderRadius: 16,
          padding: "34px 20px",
          textAlign: "center",
          cursor: "pointer",
          marginBottom: 18,
          transition: "all .16s ease"
        }
      },
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            width: 46,
            height: 46,
            borderRadius: 12,
            margin: "0 auto 12px",
            background: "rgba(40,181,207,0.12)",
            display: "grid",
            placeItems: "center"
          }
        },
        /* @__PURE__ */ React.createElement("svg", { width: "22", height: "22", viewBox: "0 0 24 24", fill: "none" }, /* @__PURE__ */ React.createElement("path", { d: "M12 16V4M12 4l-4 4M12 4l4 4", stroke: C.teal, strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" }), /* @__PURE__ */ React.createElement("path", { d: "M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2", stroke: C.teal, strokeWidth: "2", strokeLinecap: "round" }))
      ),
      /* @__PURE__ */ React.createElement("div", { style: { fontFamily: "Barlow, sans-serif", fontWeight: 600, fontSize: 17, color: C.ink } }, "Tap to upload or drop it here"),
      /* @__PURE__ */ React.createElement("div", { style: { fontFamily: "Barlow, sans-serif", fontSize: 13.5, color: C.slate, marginTop: 4 } }, "PDF or photo \xB7 from your last statement")
    ));
  }
  function ParsedReview({ fields, confidence = {}, onEdit, onConfirm, onDiscard, usd: usd2 }) {
    const loanTypes = [
      { k: "conventional", label: "Conventional" },
      { k: "fha", label: "FHA" },
      { k: "va", label: "VA" },
      { k: "usda", label: "USDA" }
    ];
    const lowCount = Object.values(confidence).filter((c) => c === "low").length;
    const flag = (key) => confidence[key] === "low" ? /* @__PURE__ */ React.createElement(
      "span",
      {
        style: {
          display: "inline-flex",
          alignItems: "center",
          gap: 4,
          fontFamily: "Barlow, sans-serif",
          fontSize: 11,
          fontWeight: 700,
          letterSpacing: "0.04em",
          textTransform: "uppercase",
          color: C.flame,
          background: "rgba(240,82,43,0.10)",
          borderRadius: 20,
          padding: "2px 8px",
          whiteSpace: "nowrap"
        }
      },
      /* @__PURE__ */ React.createElement("span", { style: { width: 5, height: 5, borderRadius: "50%", background: C.flame } }),
      "Check"
    ) : null;
    const row = (key, label, node) => {
      const low = confidence[key] === "low";
      return /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            gap: 12,
            padding: "12px 10px",
            borderRadius: 10,
            borderBottom: `1px solid ${C.line}`,
            background: low ? "rgba(240,82,43,0.04)" : "transparent"
          }
        },
        /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 8, flexShrink: 0 } }, /* @__PURE__ */ React.createElement("span", { style: { fontFamily: "Barlow, sans-serif", fontSize: 14, color: C.slate, fontWeight: 600 } }, label), flag(key)),
        /* @__PURE__ */ React.createElement("span", { style: { flex: 1, textAlign: "right" } }, node)
      );
    };
    const inlineInput = (val, onCh, prefix, suffix, ph) => /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 3, justifyContent: "flex-end" } }, prefix && /* @__PURE__ */ React.createElement("span", { style: { color: C.slate, fontFamily: "Barlow, sans-serif", fontSize: 16 } }, prefix), /* @__PURE__ */ React.createElement(
      "input",
      {
        value: val,
        placeholder: ph,
        onChange: (e) => onCh(e.target.value),
        style: {
          border: "none",
          borderBottom: `1.5px solid ${C.line}`,
          outline: "none",
          textAlign: "right",
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 16,
          color: C.ink,
          width: val && val.length > 8 ? 150 : 96,
          background: "transparent",
          padding: "2px 0"
        }
      }
    ), suffix && /* @__PURE__ */ React.createElement("span", { style: { color: C.slate, fontFamily: "Barlow, sans-serif", fontSize: 16 } }, suffix));
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Question, null, "Here\u2019s what we found."), /* @__PURE__ */ React.createElement(Helper, null, lowCount > 0 ? "Most of this came through clearly. A few fields we're less sure about are flagged \u2014 give those a quick check before we run your numbers." : "Give these a quick look and fix anything that\u2019s off before we run your numbers."), lowCount > 0 && /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          alignItems: "center",
          gap: 8,
          fontFamily: "Barlow, sans-serif",
          fontSize: 13.5,
          color: C.ink70,
          background: "rgba(240,82,43,0.06)",
          border: `1px solid rgba(240,82,43,0.25)`,
          borderRadius: 12,
          padding: "10px 14px",
          marginBottom: 14
        }
      },
      /* @__PURE__ */ React.createElement("span", { style: { width: 6, height: 6, borderRadius: "50%", background: C.flame, flexShrink: 0 } }),
      lowCount === 1 ? "1 field is worth double-checking." : `${lowCount} fields are worth double-checking.`
    ), /* @__PURE__ */ React.createElement("div", { style: { marginBottom: 20 } }, row("lender", "Lender", inlineInput(fields.lender, (v) => onEdit("lender", v), "", "", "Your lender")), row("balance", "Balance", inlineInput(fields.balance, (v) => onEdit("balance", v.replace(/[^0-9,]/g, "")), "$", "", "0")), row("rate", "Rate", inlineInput(fields.rate, (v) => onEdit("rate", v.replace(/[^0-9.]/g, "")), "", "%", "0.000")), row(
      "loanType",
      "Loan type",
      /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", gap: 6, flexWrap: "wrap", justifyContent: "flex-end" } }, loanTypes.map((t) => /* @__PURE__ */ React.createElement(
        "button",
        {
          key: t.k,
          onClick: () => onEdit("loanType", t.k),
          style: {
            padding: "5px 10px",
            borderRadius: 8,
            cursor: "pointer",
            border: `1.5px solid ${fields.loanType === t.k ? C.teal : C.line}`,
            background: fields.loanType === t.k ? "rgba(40,181,207,0.12)" : C.cardInset,
            color: fields.loanType === t.k ? C.tealDeep : C.slate,
            fontFamily: "Barlow, sans-serif",
            fontWeight: 600,
            fontSize: 13
          }
        },
        t.label
      )))
    ), row(
      "hasEscrow",
      "Escrow account",
      /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", gap: 6, justifyContent: "flex-end" } }, [{ k: true, l: "Yes" }, { k: false, l: "No" }].map((o) => /* @__PURE__ */ React.createElement(
        "button",
        {
          key: String(o.k),
          onClick: () => onEdit("hasEscrow", o.k),
          style: {
            padding: "5px 14px",
            borderRadius: 8,
            cursor: "pointer",
            border: `1.5px solid ${fields.hasEscrow === o.k ? C.teal : C.line}`,
            background: fields.hasEscrow === o.k ? "rgba(40,181,207,0.12)" : C.cardInset,
            color: fields.hasEscrow === o.k ? C.tealDeep : C.slate,
            fontFamily: "Barlow, sans-serif",
            fontWeight: 600,
            fontSize: 13
          }
        },
        o.l
      )))
    ), fields.home ? row("home", "Home value", inlineInput(fields.home, (v) => onEdit("home", v.replace(/[^0-9,]/g, "")), "$", "", "0")) : null), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 12 } }, /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onDiscard,
        style: {
          padding: "16px 20px",
          borderRadius: 14,
          border: `1.5px solid ${C.line}`,
          background: C.cardInset,
          color: C.slate,
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 15,
          cursor: "pointer"
        }
      },
      "Start over"
    ), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement(CTA, { onClick: onConfirm }, "Looks right \u2014 continue"))));
  }
  function Results({ calc, goal, show, onBack, onNext, usd: usd2 }) {
    const saveAnim = useCountUp(Math.max(calc.monthlySave, 0), show, 1100);
    const yearAnim = useCountUp(Math.max(calc.monthlySave * 12, 0), show, 1300);
    const rateLabel = calc.hasCmp ? `${calc.cmp.toFixed(3)}%` : "the rate you enter";
    const lower = calc.hasCmp && calc.monthlySave >= 40 && calc.breakEven <= 60;
    const higher = calc.hasCmp && calc.monthlySave < 0;
    const heroNum = calc.monthlySave > 0 ? Math.round(saveAnim) : 0;
    const recMap = {
      lower: {
        title: "Lower your payment",
        why: `At ${rateLabel} on a 30-year term, your estimated payment drops by about ${usd2(calc.monthlySave)}/month, with an estimated break-even near ${isFinite(calc.breakEven) ? calc.breakEven : "\u2014"} months. This is a calculation at the rate you entered, not a rate offer.`
      },
      cash: {
        title: "Take cash out",
        why: `Based on your equity, you could access up to about ${usd2(calc.maxCash)}. The figures use the ${rateLabel} comparison rate you entered \u2014 a Moxie advisor would confirm your actual rate.`
      },
      faster: {
        title: "Pay off your home faster",
        why: `At ${rateLabel} on a 20-year term, you could save roughly ${usd2(calc.interestSaved)} in total interest versus staying your current course, and be mortgage-free sooner.`
      },
      quote: {
        title: "Get a real rate first",
        why: calc.hasCmp ? `At ${rateLabel}, the numbers here are close to a wash \u2014 modest monthly change and a long break-even. Rather than guess, get an actual rate from a Moxie advisor and see if there's a better one worth acting on.` : `We didn't assume a rate for you. Enter a rate you've been quoted, or connect with a Moxie advisor to get an actual rate \u2014 then this comparison becomes real.`
      }
    };
    const rec = recMap[calc.rec];
    return /* @__PURE__ */ React.createElement(Fade, { k: "results" }, /* @__PURE__ */ React.createElement(Eyebrow, null, "Your results"), lower ? /* @__PURE__ */ React.createElement(
      "h2",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontWeight: 700,
          fontSize: "clamp(26px, 4.4vw, 40px)",
          lineHeight: 1.1,
          letterSpacing: "-0.025em",
          color: C.ink,
          margin: "0 0 10px"
        }
      },
      "At ",
      rateLabel,
      ", your payment would be about",
      " ",
      /* @__PURE__ */ React.createElement("span", { style: { color: C.flame, whiteSpace: "nowrap" } }, usd2(heroNum), "/mo lower.")
    ) : higher ? /* @__PURE__ */ React.createElement(
      "h2",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontWeight: 700,
          fontSize: "clamp(24px, 4vw, 36px)",
          lineHeight: 1.12,
          letterSpacing: "-0.02em",
          color: C.ink,
          margin: "0 0 10px"
        }
      },
      "At ",
      rateLabel,
      ", your payment would actually be higher than it is today."
    ) : /* @__PURE__ */ React.createElement(
      "h2",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontWeight: 700,
          fontSize: "clamp(24px, 4vw, 36px)",
          lineHeight: 1.12,
          letterSpacing: "-0.02em",
          color: C.ink,
          margin: "0 0 10px"
        }
      },
      "At ",
      rateLabel,
      ", refinancing may not save you much right now \u2014 and that\u2019s worth knowing too."
    ), /* @__PURE__ */ React.createElement(
      "p",
      {
        style: {
          fontFamily: "Barlow, sans-serif",
          fontSize: 14,
          color: C.slate,
          margin: "0 0 24px",
          lineHeight: 1.5
        }
      },
      "This is an estimate calculated at the ",
      calc.hasCmp ? "comparison" : "",
      " rate you entered",
      calc.hasCmp ? ` (${rateLabel})` : "",
      ". It is not a rate quote, loan offer, or approval from Moxie."
    ), calc.hasCmp && /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          alignItems: "stretch",
          gap: 12,
          marginBottom: 22,
          flexWrap: "wrap"
        }
      },
      /* @__PURE__ */ React.createElement(StatBlock, { label: "Current payment", value: usd2(calc.curPay), muted: true }),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            display: "grid",
            placeItems: "center",
            color: C.teal,
            fontSize: 28,
            fontWeight: 700,
            minWidth: 30
          }
        },
        calc.monthlySave >= 0 ? "\u2193" : "\u2191"
      ),
      /* @__PURE__ */ React.createElement(StatBlock, { label: `Payment at ${rateLabel}`, value: usd2(calc.pay30), accent: true }),
      calc.monthlySave > 0 ? /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            flexBasis: "100%",
            fontFamily: "Barlow, sans-serif",
            fontSize: 17,
            color: C.ink70,
            marginTop: 4
          }
        },
        "That\u2019s approximately",
        " ",
        /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, usd2(Math.round(yearAnim)), "/year"),
        " ",
        "at this rate."
      ) : /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            flexBasis: "100%",
            fontFamily: "Barlow, sans-serif",
            fontSize: 17,
            color: C.ink70,
            marginTop: 4
          }
        },
        "At this rate a refinance would cost about",
        " ",
        /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, usd2(Math.abs(Math.round(calc.monthlySave))), "/mo more"),
        " ",
        "than your current payment."
      )
    ), lower && (() => {
      const annual = Math.round(calc.monthlySave * 12);
      const be = calc.breakEven;
      const tier = be <= 24 ? "strong" : be <= 48 ? "solid" : "long";
      const eyebrow = tier === "strong" ? "Money back in your budget" : tier === "solid" ? "Real monthly breathing room" : "What this looks like over time";
      const beLine = tier === "strong" ? /* @__PURE__ */ React.createElement(React.Fragment, null, "Your savings start the very first month, and you\u2019re fully ahead of costs in about ", /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, be, " months"), ".") : tier === "solid" ? /* @__PURE__ */ React.createElement(React.Fragment, null, "You start saving right away, and you\u2019re fully ahead of costs in about ", /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, be, " months"), ".") : /* @__PURE__ */ React.createElement(React.Fragment, null, "Your savings begin the first month. Because it takes about ", /* @__PURE__ */ React.createElement("strong", { style: { color: C.ink } }, be, " months"), " to fully cover costs, this one makes the most sense if you plan to keep the home past then.");
      return /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            background: C.surface,
            borderRadius: 16,
            padding: "20px 22px",
            marginBottom: 26,
            border: `1px solid ${C.line}`
          }
        },
        /* @__PURE__ */ React.createElement(
          "div",
          {
            style: {
              fontFamily: "Barlow Condensed, Barlow, sans-serif",
              fontWeight: 700,
              fontSize: 14,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
              color: C.tealDeep,
              marginBottom: 10
            }
          },
          eyebrow
        ),
        /* @__PURE__ */ React.createElement(
          "div",
          {
            style: {
              fontFamily: "Barlow, sans-serif",
              fontSize: 18,
              color: C.ink,
              lineHeight: 1.45,
              marginBottom: 12
            }
          },
          "You\u2019d keep about",
          " ",
          /* @__PURE__ */ React.createElement("strong", { style: { color: C.flame } }, usd2(calc.monthlySave), " more every month"),
          " ",
          "\u2014 roughly",
          " ",
          /* @__PURE__ */ React.createElement("strong", null, usd2(annual), " a year"),
          " back in your budget."
        ),
        /* @__PURE__ */ React.createElement("p", { style: { margin: "0 0 16px", fontSize: 15, color: C.ink70, lineHeight: 1.5 } }, beLine, " ", "Most borrowers roll refinance costs into the loan, so there\u2019s often little or nothing due up front.", " ", /* @__PURE__ */ React.createElement("span", { style: { color: C.slate } }, "(Est. costs ~", usd2(calc.costs), ", typically financed. Full breakdown below.)")),
        /* @__PURE__ */ React.createElement(BreakEvenMeter, { months: calc.breakEven, show })
      );
    })(), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          fontFamily: "Barlow Condensed, Barlow, sans-serif",
          fontWeight: 700,
          fontSize: 15,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          color: C.ink,
          margin: "6px 0 14px"
        }
      },
      "Your options"
    ), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: 12,
          marginBottom: 26
        }
      },
      /* @__PURE__ */ React.createElement(
        OptionCard,
        {
          title: "Lower your payment",
          big: calc.monthlySave > 0 ? `${usd2(calc.monthlySave)}/mo less` : `${usd2(Math.abs(calc.monthlySave))}/mo more`,
          detail: `30-year fixed at ${rateLabel}`,
          recommended: calc.rec === "lower",
          dim: !lower
        }
      ),
      /* @__PURE__ */ React.createElement(
        OptionCard,
        {
          title: "Pay off faster",
          big: calc.interestSaved > 0 ? `~${usd2(calc.interestSaved)} interest saved` : "Depends on rate",
          detail: `20-year fixed at ${rateLabel}`,
          recommended: calc.rec === "faster"
        }
      ),
      /* @__PURE__ */ React.createElement(
        OptionCard,
        {
          title: "Take cash out",
          big: `Up to ${usd2(calc.maxCash)}`,
          detail: calc.cashPay ? `Payment ~${usd2(calc.cashPay)}/mo at ${rateLabel}` : "Based on your equity",
          recommended: calc.rec === "cash"
        }
      )
    ), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          borderRadius: 16,
          padding: "20px 22px",
          background: "linear-gradient(135deg, rgba(40,181,207,0.10), rgba(40,181,207,0.03))",
          border: `1.5px solid rgba(40,181,207,0.35)`,
          marginBottom: 26
        }
      },
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow Condensed, Barlow, sans-serif",
            fontWeight: 700,
            fontSize: 14,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            color: C.tealDeep,
            marginBottom: 8
          }
        },
        "Our most interesting option for you"
      ),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow, sans-serif",
            fontWeight: 700,
            fontSize: 22,
            color: C.ink,
            marginBottom: 6
          }
        },
        rec.title
      ),
      /* @__PURE__ */ React.createElement("p", { style: { margin: 0, fontSize: 15.5, color: C.ink70, lineHeight: 1.5 } }, rec.why)
    ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 24 } }, /* @__PURE__ */ React.createElement(CTA, { tone: "flame", onClick: onNext }, "See my real options")), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12 } }, /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onBack,
        style: {
          width: "100%",
          padding: "12px",
          border: "none",
          background: "transparent",
          color: C.slate,
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 15,
          cursor: "pointer"
        }
      },
      "Adjust my numbers"
    )), /* @__PURE__ */ React.createElement(AssumptionsNote, { calc, rateLabel, usd: usd2 }));
  }
  function StatBlock({ label, value, muted, accent }) {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          flex: 1,
          minWidth: 120,
          background: accent ? "rgba(40,181,207,0.08)" : C.surface,
          border: `1px solid ${accent ? "rgba(40,181,207,0.3)" : C.line}`,
          borderRadius: 14,
          padding: "16px 18px"
        }
      },
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow, sans-serif",
            fontSize: 13,
            fontWeight: 600,
            color: C.slate,
            marginBottom: 4,
            letterSpacing: "0.02em"
          }
        },
        label
      ),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow Condensed, Barlow, sans-serif",
            fontWeight: 700,
            fontSize: 34,
            color: accent ? C.tealDeep : muted ? C.ink70 : C.ink,
            letterSpacing: "-0.01em",
            fontVariantNumeric: "tabular-nums"
          }
        },
        value
      )
    );
  }
  function BreakEvenMeter({ months, show }) {
    const cap = 60;
    const pct = Math.min(months / cap * 100, 100);
    return /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          position: "relative",
          height: 10,
          borderRadius: 6,
          background: "linear-gradient(90deg, rgba(40,181,207,0.25), rgba(40,181,207,0.08))",
          overflow: "hidden"
        }
      },
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            position: "absolute",
            left: 0,
            top: 0,
            bottom: 0,
            width: show ? `${pct}%` : "0%",
            background: C.teal,
            borderRadius: 6,
            transition: "width 1.1s cubic-bezier(.22,.61,.36,1)"
          }
        }
      ),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            position: "absolute",
            left: show ? `${pct}%` : "0%",
            top: -3,
            width: 4,
            height: 16,
            borderRadius: 2,
            background: C.navy,
            transition: "left 1.1s cubic-bezier(.22,.61,.36,1)"
          }
        }
      )
    ), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          justifyContent: "space-between",
          marginTop: 8,
          fontFamily: "Barlow, sans-serif",
          fontSize: 12.5,
          color: C.slate,
          fontWeight: 500
        }
      },
      /* @__PURE__ */ React.createElement("span", null, "Today"),
      /* @__PURE__ */ React.createElement("span", { style: { color: C.ink, fontWeight: 700 } }, "Break-even \xB7 month ", months),
      /* @__PURE__ */ React.createElement("span", null, "5 yrs")
    ));
  }
  function OptionCard({ title, big, detail, recommended, dim }) {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          borderRadius: 16,
          padding: "18px 18px 16px",
          background: C.cardInset,
          border: `1.5px solid ${recommended ? C.teal : C.line}`,
          boxShadow: recommended ? "0 12px 30px rgba(40,181,207,0.16)" : "none",
          opacity: dim ? 0.6 : 1,
          position: "relative",
          display: "flex",
          flexDirection: "column",
          gap: 4
        }
      },
      recommended && /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            position: "absolute",
            top: -10,
            left: 16,
            background: C.teal,
            color: C.white,
            fontFamily: "Barlow Condensed, Barlow, sans-serif",
            fontWeight: 700,
            fontSize: 11,
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            padding: "3px 10px",
            borderRadius: 20
          }
        },
        "Recommended"
      ),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow, sans-serif",
            fontWeight: 600,
            fontSize: 14,
            color: C.slate,
            marginTop: recommended ? 6 : 0
          }
        },
        title
      ),
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            fontFamily: "Barlow Condensed, Barlow, sans-serif",
            fontWeight: 700,
            fontSize: 26,
            color: C.ink,
            lineHeight: 1.05,
            letterSpacing: "-0.01em"
          }
        },
        big
      ),
      /* @__PURE__ */ React.createElement("div", { style: { fontFamily: "Barlow, sans-serif", fontSize: 13, color: C.slate, lineHeight: 1.4 } }, detail)
    );
  }
  function AssumptionsNote({ calc, rateLabel, usd: usd2 }) {
    const [open, setOpen] = useState(false);
    const sub = {
      fontFamily: "Barlow, sans-serif",
      fontWeight: 700,
      fontSize: 12,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: C.slate,
      margin: "14px 0 4px"
    };
    const body = {
      margin: 0,
      fontSize: 13.5,
      lineHeight: 1.55,
      color: C.slate,
      fontFamily: "Barlow, sans-serif"
    };
    return /* @__PURE__ */ React.createElement("div", { style: { marginTop: 22 } }, /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => setOpen((o) => !o),
        style: {
          width: "100%",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 6,
          padding: "8px 2px",
          background: "transparent",
          border: "none",
          cursor: "pointer",
          fontFamily: "Barlow, sans-serif",
          fontWeight: 600,
          fontSize: 13,
          color: C.slate
        }
      },
      "Assumptions",
      /* @__PURE__ */ React.createElement(
        "span",
        {
          style: {
            transform: open ? "rotate(180deg)" : "rotate(0)",
            transition: "transform .2s ease",
            fontSize: 11,
            lineHeight: 1
          }
        },
        "\u25BE"
      )
    ), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          maxHeight: open ? 600 : 0,
          overflow: "hidden",
          transition: "max-height .35s ease"
        }
      },
      /* @__PURE__ */ React.createElement(
        "div",
        {
          style: {
            background: C.surface,
            border: `1px solid ${C.line}`,
            borderRadius: 12,
            padding: "4px 16px 16px",
            marginTop: 6
          }
        },
        /* @__PURE__ */ React.createElement("div", { style: sub }, "How this is calculated"),
        /* @__PURE__ */ React.createElement("p", { style: body }, "We take the balance, current rate, and remaining term you entered to compute your current payment, then recompute it at the ", rateLabel, " ", "comparison rate you provided \u2014 we don\u2019t assume or predict a rate. Estimated cost to refinance (about ", usd2(calc.costs), ") covers lender and third-party fees, roughly 0.9% of balance plus ~$1,300 for appraisal, title, and recording. Break-even is that cost divided by your estimated monthly savings."),
        /* @__PURE__ */ React.createElement("div", { style: sub }, "What we assumed"),
        /* @__PURE__ */ React.createElement("p", { style: body }, "Roughly ", calc.yrsLeft, " years remaining on your current loan, a full-balance refinance, and the ", rateLabel, " rate you entered.", " ", calc.escrowWaived ? "Because this looks like a conventional loan at 80% loan-to-value or below, we assumed escrows can be waived, so the cost estimate leaves out prepaid taxes and insurance (those fund a new escrow and are largely offset by the refund from your existing one)." : "Because escrows look required here (FHA, VA, or USDA, or loan-to-value above 80%), we included an estimate for funding a new escrow account up front; your existing escrow balance is typically refunded separately after closing.", " ", "Costs are assumed rolled into the loan; cash-out assumes lending up to 80% of your home\u2019s value."),
        /* @__PURE__ */ React.createElement("div", { style: sub }, "What could change these numbers"),
        /* @__PURE__ */ React.createElement("p", { style: body }, "Your actual rate depends on credit, loan-to-value, property type, income, and market conditions, and may differ from the rate you entered. Actual closing costs, escrow setup, and prepaid interest vary by lender and closing date. Nothing here is a rate lock, offer, or approval; a Moxie advisor confirms real numbers for your situation.")
      )
    ));
  }
  function StyleTag() {
    return /* @__PURE__ */ React.createElement("style", null, `
      @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&display=swap');
      .moxie-numfield::placeholder {
        font-size: 26px;
        font-weight: 500;
        color: #6b7684;
        opacity: 1;
        letter-spacing: -0.01em;
      }
      .moxie-numfield::-webkit-input-placeholder {
        font-size: 26px;
        font-weight: 500;
        color: #6b7684;
        opacity: 1;
      }
      @keyframes moxieIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
      @keyframes moxiePop {
        0% { transform: scale(0.6); opacity: 0; }
        60% { transform: scale(1.08); }
        100% { transform: scale(1); opacity: 1; }
      }
      @keyframes moxieSpin {
        to { transform: rotate(360deg); }
      }
      @media (prefers-reduced-motion: reduce) {
        * { animation: none !important; transition: none !important; }
      }
    `);
  }
  const MOXIE_LOGO_DARK = "data:image/png;base64,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";
  window.MoxieRefinance = MoxieRefinance;
})();

  