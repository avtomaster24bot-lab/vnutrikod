/* Внутрикод — общая логика: космос-фон, появление блоков, цены из config.js, UTM, окно записи → Telegram Марины,
   прогресс «Мой путь» (localStorage), подарок перед уходом, энциклопедия, статьи. Без фреймворков. */
(function(){
  "use strict";
  document.documentElement.classList.remove("no-js");
  var C = window.SITE_CONFIG || {}, VK = window.VK || {prods:{}, arts:{}};
  var P = C.prices || {}, D = C.dates || {}, K = C.contacts || {};
  var ROOT = document.body.dataset.root || "", PAGE = document.body.dataset.page || "home";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(s, r){ return (r||document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); }
  function val(map, code, group){ return (code && map[code]) || (group && map[group]) || ""; }
  function price(code, group){ return val(P, code, group) || C.defaultPrice || "Цена уточняется"; }
  function date(code, group){ return val(D, code, group) || C.defaultDate || "Дата уточняется"; }
  function esc(s){ return String(s).replace(/[&<>"']/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }

  /* ---------- Космос: лёгкие частицы-нейроны на canvas ---------- */
  (function(){
    var cv = document.getElementById("cosmos"); if(!cv || !cv.getContext) return;
    var ctx = cv.getContext("2d"), W, H, pts = [], raf = 0, dpr = Math.min(window.devicePixelRatio||1, 2), mx = -999, my = -999;
    function size(){ W = innerWidth; H = innerHeight; cv.width = W*dpr; cv.height = H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
      var n = Math.round(Math.min(90, W*H/16000)); pts = [];
      for(var i=0;i<n;i++) pts.push({x:Math.random()*W, y:Math.random()*H, vx:(Math.random()-.5)*.25, vy:(Math.random()-.5)*.25, r:Math.random()*1.6+.4, h:[186,258,316][i%3]});
    }
    function draw(){
      ctx.clearRect(0,0,W,H);
      for(var i=0;i<pts.length;i++){ var p = pts[i];
        if(!reduce){ p.x += p.vx; p.y += p.vy; if(p.x<0||p.x>W) p.vx*=-1; if(p.y<0||p.y>H) p.vy*=-1; }
        for(var j=i+1;j<pts.length;j++){ var q = pts[j], dx = p.x-q.x, dy = p.y-q.y, d = dx*dx+dy*dy;
          if(d < 15000){ ctx.strokeStyle = "hsla("+p.h+",90%,70%,"+(0.16*(1-d/15000))+")"; ctx.lineWidth = .7; ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke(); } }
        var md = (p.x-mx)*(p.x-mx)+(p.y-my)*(p.y-my), g = md < 22000 ? 2 : 1;
        ctx.fillStyle = "hsla("+p.h+",95%,75%,"+(0.55*g)+")"; ctx.beginPath(); ctx.arc(p.x,p.y,p.r*g,0,6.283); ctx.fill();
      }
      if(!reduce && !document.hidden) raf = requestAnimationFrame(draw);
    }
    size(); draw();
    addEventListener("resize", function(){ cancelAnimationFrame(raf); size(); draw(); });
    addEventListener("pointermove", function(e){ mx = e.clientX; my = e.clientY; }, {passive:true});
    document.addEventListener("visibilitychange", function(){ if(!document.hidden && !reduce){ cancelAnimationFrame(raf); draw(); } });
  })();

  /* ---------- Появление блоков при прокрутке ---------- */
  function reveal(scope){
    var els = $$(".rv:not(.in)", scope);
    if(reduce || !("IntersectionObserver" in window)){ els.forEach(function(el){ el.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function(en){ en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add("in"); io.unobserve(x.target); } }); }, {rootMargin:"0px 0px -6% 0px"});
    els.forEach(function(el){ io.observe(el); });
  }
  reveal();

  /* ---------- Меню ---------- */
  var b = $(".burger"), n = $(".nav");
  if(b && n) b.addEventListener("click", function(){ n.classList.toggle("open"); b.setAttribute("aria-expanded", n.classList.contains("open")); });

  /* ---------- Цены, даты, выгода — из config.js ---------- */
  $$("[data-price]").forEach(function(el){ el.textContent = price(el.dataset.price, el.dataset.group); });
  $$("[data-date]").forEach(function(el){ el.textContent = date(el.dataset.date, el.dataset.group); });
  $$("[data-pnote]").forEach(function(el){ var v = (C.priceNotes||{})[el.dataset.pnote]; if(v) el.textContent = v; });
  $$("[data-upgrade]").forEach(function(el){ if(C.upgradeNote) el.textContent = C.upgradeNote; });
  function num(code, group){ var v = val(P, code, group); if(!v || /[–-]/.test(v)) return 0; return parseInt(v.replace(/\D/g,""),10) || 0; }
  function rub(x){ return x.toLocaleString("ru-RU").replace(/\u00a0/g," ") + " ₽"; }
  $$("[data-save]").forEach(function(el){
    var k = el.dataset.save, code = el.dataset.code, tr = num("training"), md = num("module"), t = "";
    if(k==="module"){ var a = 4*tr - md; if(tr && md && a>0) t = "Выгода " + rub(a) + " по сравнению с 4 тренингами по отдельности."; }
    if(k==="full"){ var f = num("koleso-full"), p1 = num("koleso-part1"), p2 = num("koleso-part2"), c = p1+p2-f, c3 = 6*md - f;
      if(f && p1 && p2 && c>0) t = "Выгода " + rub(c) + " по сравнению с двумя частями" + (md && c3>0 ? " и " + rub(c3) + " — с 6 модулями по отдельности." : "."); }
    if(k==="pkg"){ var one = num("individ-sessiya"), pk = num(code), nn = +el.dataset.n || 0, g = nn*one - pk;
      if(one && pk && g>0) t = "Выгода " + rub(g) + " по сравнению с " + nn + " сессиями по " + rub(one) + "."; }
    el.textContent = t;
  });
  $$("[data-link]").forEach(function(el){ var u = K[el.dataset.link]; if(u){ el.href = u; el.classList.remove("hidden"); } else el.classList.add("hidden"); });

  /* ---------- UTM: откуда пришёл человек ---------- */
  var qs = new URLSearchParams(location.search), utm = {};
  ["utm_source","utm_medium","utm_campaign","utm_content","utm_term"].forEach(function(k){ if(qs.get(k)) utm[k] = qs.get(k); });
  try{ if(Object.keys(utm).length) localStorage.setItem("vk_utm", JSON.stringify(utm)); else utm = JSON.parse(localStorage.getItem("vk_utm")||"{}"); }catch(e){}

  /* ---------- Прогресс «Мой путь» ---------- */
  var KEY = "vk_path_v1";
  function load(){ try{ return JSON.parse(localStorage.getItem(KEY)) || {}; }catch(e){ return {}; } }
  var S = load(); ["arts","tests","done","gifts","ch"].forEach(function(k){ S[k] = S[k] || {}; });
  function save(){ try{ localStorage.setItem(KEY, JSON.stringify(S)); }catch(e){} paintLevel(); }
  function points(){ return 10*Object.keys(S.arts).length + 20*Object.keys(S.tests).length + 15*Object.keys(S.done).length + 10*Object.keys(S.gifts).length + 10*Object.keys(S.ch).length + (S.route ? 15 : 0); }
  var LEVELS = ["Исследователь","Наблюдатель","Искатель","Практик","Навигатор","Архитектор","Мастер внутреннего кода"];
  function level(){ var pt = points(), l = Math.min(LEVELS.length, 1 + Math.floor(pt/60)); return {n:l, name:LEVELS[l-1], pts:pt, pct: l>=LEVELS.length ? 100 : Math.round((pt % 60)/60*100)}; }
  function paintLevel(){ var L = level(); $$("[data-lvl]").forEach(function(el){ el.textContent = L.n; el.title = "Уровень " + L.n + ": " + L.name; }); }
  function award(kind, id, data){ var fresh = !S[kind][id]; S[kind][id] = data || Date.now(); if(kind==="route") S.route = data; save(); if(fresh && kind!=="arts") toast("+" + ({tests:20,done:15,gifts:10,ch:10}[kind]||10) + " к пути · уровень " + level().n); return fresh; }
  paintLevel();
  $$("[data-art]").forEach(function(el){ if(S.arts[el.dataset.art]) el.classList.add("is-seen"); });
  $$("[data-testlink]").forEach(function(el){ if(S.tests[el.dataset.testlink]) el.classList.add("is-seen"); });

  /* ---------- Тосты ---------- */
  var tEl = document.getElementById("toast"), tt;
  function toast(t){ if(!tEl) return; tEl.textContent = t; tEl.classList.add("show"); clearTimeout(tt); tt = setTimeout(function(){ tEl.classList.remove("show"); }, 4500); }

  /* ---------- Кнопки записи → окно → Telegram Марины ---------- */
  var TG = K.marinaTelegram || "https://t.me/MarinaNew";
  function buildMsg(el){
    var head = el.dataset.head || "", tail = el.dataset.tail || "", pr = "";
    if(el.dataset.noprice === undefined){ var v = val(P, el.dataset.cta, el.dataset.group); if(v) pr = " Цена на сайте: " + v + "."; }
    var src = [utm.utm_source, utm.utm_campaign, utm.utm_content].filter(Boolean).join(" / ");
    return head + pr + (tail ? " " + tail : "") + "\n(источник: сайт " + (C.brand || "Внутрикод") + (src ? " / " + src : "") + ")";
  }
  function initCta(scope){ $$("[data-cta]", scope).forEach(function(el){ el.href = TG + "?text=" + encodeURIComponent(buildMsg(el)); el.target = "_blank"; el.rel = "noopener"; }); }
  initCta();
  function ctaHtml(key, label, cls){
    var p = VK.prods[key]; if(!p) return "";
    return '<a class="' + (cls||"btn") + '" href="' + TG + '" data-cta="' + esc(p.code) + '" data-group="' + esc(p.g) + '" data-title="' + esc(p.t) + '" data-head="' + esc(p.head) + '" data-tail="' + esc(p.tail) + '"' + (p.np ? " data-noprice" : "") + '>' + esc(label || ("Записаться · " + price(p.code, p.g))) + '</a>';
  }
  function copyText(t, okEl){
    function done(){ if(okEl) okEl.textContent = "Текст скопирован. Если в Telegram он не подставился — просто вставьте его в чат."; else toast("Текст скопирован"); }
    try{ if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(done, fallback); return; } }catch(e){}
    fallback();
    function fallback(){ var ta = document.createElement("textarea"); ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); try{ document.execCommand("copy"); done(); }catch(e){} ta.remove(); }
  }
  var modal = document.getElementById("cta-modal"), lastFocus = null;
  function openModal(el){
    var code = el.dataset.cta, group = el.dataset.group, msg = buildMsg(el), url = TG + "?text=" + encodeURIComponent(msg);
    $("[data-m-title]", modal).textContent = el.dataset.title || document.title;
    $("[data-m-price]", modal).textContent = el.dataset.noprice !== undefined ? "обсуждается лично" : price(code, group);
    $("[data-m-date]", modal).textContent = date(code, group);
    $("[data-m-msg]", modal).textContent = msg;
    var tg = $("[data-m-tg]", modal); tg.href = url;
    var pay = $("[data-m-pay]", modal), pl = (C.paymentLinks||{})[code];
    if(pl){ pay.href = pl; pay.classList.remove("hidden"); } else pay.classList.add("hidden");
    $("[data-m-paynote]", modal).textContent = pl ? "Можно оплатить онлайн или написать Марине." : "Напишите Марине — она пришлёт детали для оплаты.";
    $(".ok", modal).textContent = ""; modal.dataset.msg = msg;
    lastFocus = el; modal.classList.add("open"); tg.focus();
    goal("cta_click", {product: code});
  }
  function closeModal(){ if(modal && modal.classList.contains("open")){ modal.classList.remove("open"); if(lastFocus) lastFocus.focus(); } }
  document.addEventListener("click", function(e){
    var el = e.target.closest("[data-cta]");
    if(el){ if(modal){ e.preventDefault(); openModal(el); } return; }
    if(!modal) return;
    if(e.target === modal || e.target.closest("#cta-modal .mclose")){ closeModal(); return; }
    if(e.target.closest("[data-m-tg]")){ copyText(modal.dataset.msg, $(".ok", modal)); goal("tg_click"); }
    if(e.target.closest("[data-m-copy]")) copyText(modal.dataset.msg, $(".ok", modal));
  });
  document.addEventListener("keydown", function(e){ if(e.key === "Escape"){ closeModal(); hideGift(); } });

  /* ---------- Яндекс.Метрика (если указан номер счётчика) ---------- */
  function goal(g, p){ try{ if(window.ym && C.yandexMetrikaId) ym(+C.yandexMetrikaId, "reachGoal", g, p); }catch(e){} }
  if(C.yandexMetrikaId){
    (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})(window,document,"script","https://mc.yandex.ru/metrika/tag.js?id="+C.yandexMetrikaId,"ym");
    ym(+C.yandexMetrikaId, "init", {ssr:true, clickmap:true, referrer:document.referrer, url:location.href, accurateTrackBounce:true, trackLinks:true});
  }

  /* ---------- Подарок перед уходом (1 раз за сессию) ---------- */
  var gp = document.getElementById("giftpop"), gpShown = false, t0 = Date.now();
  function giftAllowed(){ if(!gp || gpShown) return false; if(/^(testy\/|moj-put|navigator|404)/.test(PAGE)) return false; try{ if(sessionStorage.getItem("vk_gift")) return false; }catch(e){} return Date.now() - t0 > 15000 && !(modal && modal.classList.contains("open")); }
  function showGift(){
    if(!giftAllowed()) return; gpShown = true; try{ sessionStorage.setItem("vk_gift","1"); }catch(e){}
    var go = $("[data-gp-go]", gp);
    if(S.tests.tormoza){ $("#gp-t").textContent = "Вытяните карту дня — вопрос, который стоит задать себе сегодня"; $("p", gp).textContent = "Генеративная карта и вопрос для самоисследования. Бесплатно."; go.textContent = "Открыть карту"; go.href = ROOT + "karta-dnya/"; }
    else go.href = ROOT + "testy/tormoza/";
    gp.hidden = false; goal("gift_prompt");
  }
  function hideGift(){ if(gp) gp.hidden = true; }
  if(gp){
    gp.addEventListener("click", function(e){ if(e.target.closest("[data-gp-close]")) hideGift(); });
    document.addEventListener("mouseout", function(e){ if(!e.relatedTarget && e.clientY < 8) showGift(); });
    addEventListener("scroll", function(){ var h = document.documentElement; if((h.scrollTop + innerHeight) / h.scrollHeight > .7) showGift(); }, {passive:true});
  }

  /* ---------- Энциклопедия: поиск и фильтр ---------- */
  var enc = document.getElementById("enc");
  if(enc){
    var q = $("#encq"), cat = qs.get("cat") || "all", items = $$(".encit", enc);
    function apply(){
      var s = (q.value || "").trim().toLowerCase(), shown = 0;
      items.forEach(function(it){ var ok = (cat==="all" || it.dataset.c===cat) && (!s || it.dataset.q.indexOf(s) > -1); it.classList.toggle("hidden", !ok); if(ok) shown++; });
      $$(".fchip").forEach(function(c){ c.classList.toggle("on", c.dataset.cat===cat); });
      $("#encstat").textContent = "Статей: " + shown + " из " + items.length + " · прочитано: " + Object.keys(S.arts).length;
      $("#encempty").classList.toggle("hidden", shown > 0);
      $$(".encit:not(.hidden) .rv").forEach(function(el){ el.classList.add("in"); });
    }
    $$(".fchip").forEach(function(c){ c.addEventListener("click", function(){ cat = c.dataset.cat; var u = new URL(location.href); if(cat==="all") u.searchParams.delete("cat"); else u.searchParams.set("cat", cat); history.replaceState(null, "", u); apply(); }); });
    q.addEventListener("input", apply); apply();
  }

  /* ---------- Статья: прогресс чтения, чек-лист, практика ---------- */
  var art = $("[data-article]");
  if(art){
    var slug = art.dataset.article, bar = $(".readbar i", art), marked = false;
    addEventListener("scroll", function(){
      var r = art.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight)));
      if(bar) bar.style.width = (p*100) + "%";
      if(p > .6 && !marked){ marked = true; if(award("arts", slug)) toast("Статья засчитана в «Мой путь» · +10"); }
    }, {passive:true});
    var boxes = $$("[data-sign]", art), res = $("[data-signres]", art);
    function cnt(){ var c = boxes.filter(function(x){ return x.checked; }).length, t = "Отмечено: " + c + " из " + boxes.length + ". ";
      if(c >= Math.ceil(boxes.length*0.6)) t += "Похоже, тема вам очень знакома. Это не диагноз, а повод присмотреться — тест и живой разбор помогут увидеть картину целиком.";
      else if(c >= 2) t += "Некоторые признаки откликаются — практика ниже поможет понаблюдать за ними.";
      res.textContent = t; }
    boxes.forEach(function(x){ x.addEventListener("change", cnt); });
    $$("[data-done]", art).forEach(function(btn){
      if(S.done[btn.dataset.done]){ btn.textContent = "Практика выполнена ✓"; }
      btn.addEventListener("click", function(){ award("done", btn.dataset.done); btn.textContent = "Практика выполнена ✓"; });
    });
  }

  /* ---------- PDF: засчитываем как подарок ---------- */
  $$("[data-pdf]").forEach(function(a){ a.addEventListener("click", function(){ award("gifts", "pdf"); }); });

  window.VKA = {S:S, save:save, award:award, level:level, LEVELS:LEVELS, points:points, toast:toast, ctaHtml:ctaHtml, initCta:initCta, reveal:reveal, price:price, esc:esc, root:ROOT, page:PAGE, reduce:reduce, goal:goal};
})();
