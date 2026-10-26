/* Внутрикод — интерактивные инструменты: Навигатор (ИИ + сценарий), тесты, карта дня, Мини-Лила, дыхание, челлендж, «Мой путь».
   Всё работает офлайн в браузере. ИИ подключается только через config.aiEndpoint (сервер-прокси); ключей во фронтенде нет. */
(function(){
  "use strict";
  var A = window.VKA, VK = window.VK || {}, C = window.SITE_CONFIG || {};
  if(!A) return;
  var R = A.root, esc = A.esc;
  function $(s, r){ return (r||document).querySelector(s); }
  function $$(s, r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); }
  function artLink(s){ var a = VK.arts[s]; return a ? '<a href="' + R + 'znaniya/' + s + '/"><span>' + esc(a.t) + '<small>Статья · ' + esc(a.c) + '</small></span></a>' : ""; }
  function prodUrl(k){ var p = VK.prods[k]; return p ? R + p.u : R + "ceny/"; }
  var TEST = {}; (VK.tests||[]).forEach(function(t){ TEST[t.slug] = t; });
  function safeUrl(u){ u = String(u||""); if(/^(https?:)?\/\//i.test(u) || /^[\/#a-z0-9._-]/i.test(u) && !/^\s*(javascript|data|vbscript):/i.test(u)) return u; return "#"; }

  /* ===================== НАВИГАТОР ===================== */
  $$("[data-navigator]").forEach(function(box){
    var log = $("[data-nv-log]", box), opts = $("[data-nv-opts]", box), form = $("[data-nv-form]", box), inp = $("[data-nv-input]", box), modeEl = $("[data-nv-mode]", box);
    var EP = (C.aiEndpoint || "").trim(), aiOn = !!EP, history = [], st = {};
    function setMode(ai){ aiOn = ai; modeEl.textContent = ai ? "ИИ-помощник" : "Навигатор"; modeEl.classList.toggle("ai", ai); modeEl.title = ai ? "Ответы формирует ИИ-помощник через сервер Внутрикода" : "Работает по готовому сценарию прямо в браузере"; }
    setMode(aiOn);
    function say(html, who, plain){ var d = document.createElement("div"); d.className = "msg " + (who||"bot"); if(plain) d.textContent = html; else d.innerHTML = html; log.appendChild(d); log.scrollTop = log.scrollHeight; history.push({role: who==="me" ? "user" : "assistant", content: d.textContent}); if(history.length > 20) history = history.slice(-20); return d; }
    function choices(list){ opts.innerHTML = ""; list.forEach(function(c){ var b = document.createElement("button"); b.type = "button"; b.textContent = c[0]; b.addEventListener("click", function(){ say(c[0], "me", true); opts.innerHTML = ""; setTimeout(c[1], A.reduce ? 0 : 350); }); opts.appendChild(b); }); }
    var TH = VK.themes || {};
    function askTheme(intro){
      say(intro || "Привет! Я помогу собрать личный маршрут: подарок, статью, тест и живой шаг. <b>Что сейчас ближе всего?</b>");
      choices(Object.keys(TH).map(function(k){ return [TH[k].label, function(){ st.theme = k; askLevel(); }]; }).concat([["Не знаю — помогите разобраться", function(){ st.theme = "celi"; st.unsure = true; askLevel(); }]]));
    }
    function askLevel(){ say("Насколько сильно это мешает сейчас?"); choices([["Слегка, хочется разобраться", function(){ st.lvl = 1; askStart(); }], ["Заметно, повторяется снова и снова", function(){ st.lvl = 2; askStart(); }], ["Очень сильно и давно", function(){ st.lvl = 3; askStart(); }]]); }
    function askStart(){ say("Как вам удобнее начать?"); choices([["Почитать и разобраться самой", function(){ st.start = "read"; askTime(); }], ["Пройти тест и получить разбор", function(){ st.start = "test"; askTime(); }], ["Сразу живой шаг с Мариной", function(){ st.start = "live"; askTime(); }]]); }
    function askTime(){ say("И последнее: сколько времени готовы вложить в ближайшую неделю?"); choices([["5–15 минут", function(){ st.time = 1; route(); }], ["1–3 часа", function(){ st.time = 2; route(); }], ["Готова к работе на месяц и больше", function(){ st.time = 3; route(); }]]); }
    function route(){
      var th = TH[st.theme], items = [], live = [];
      var gift = (VK.gifts||[]).filter(function(g){ return g[0] === th.gift + "/"; })[0];
      var test = TEST[th.test];
      var aL = th.articles.map(artLink).join("");
      var gL = gift ? '<a href="' + R + gift[0] + '"><span>' + gift[1] + " " + esc(gift[2]) + '<small>Бесплатный подарок</small></span></a>' : "";
      var tL = test ? '<a href="' + R + 'testy/' + test.slug + '/"><span>' + test.emoji + " Тест «" + esc(test.title) + '»<small>Бесплатно · ' + test.mins + ' мин</small></span></a>' : "";
      if(st.start === "read") items = [artLink(th.articles[0]), gL, tL, artLink(th.articles[1])];
      else if(st.start === "test") items = [tL, artLink(th.articles[0]), gL];
      else items = [tL, artLink(th.articles[0])];
      var main = (st.lvl === 3 || st.start === "live" || st.time === 3) ? "diag" : th.mini, more = st.time === 3 ? th.module : th.deep;
      [main, more].forEach(function(k){ var p = VK.prods[k]; if(p) live.push('<a href="' + prodUrl(k) + '"><span>' + esc(p.t) + '<small>' + esc(p.k || "Живой шаг с Мариной") + ' · ' + esc(A.price(p.code, p.g)) + '</small></span></a>'); });
      var html = "<b>Ваш маршрут готов.</b> Тема: «" + esc(th.label) + "».<div class='route'>" + items.filter(Boolean).join("") + live.join("") + "</div>";
      if(st.lvl === 3) html += "<p class='small'>Если состояние совсем тяжёлое, важно не оставаться с этим одной — вот <a href='" + R + "vazhno/#help'>контакты срочной помощи</a>.</p>";
      say(html);
      var c = document.createElement("div"); c.className = "msg bot"; c.innerHTML = "Хотите живой шаг прямо сейчас? <div class='btns'>" + A.ctaHtml(main, null, "btn sm") + "<a class='btn ghost sm' href='" + R + "moj-put/'>Маршрут сохранён в «Мой путь»</a></div>"; log.appendChild(c); A.initCta(c); log.scrollTop = log.scrollHeight;
      A.S.route = {theme: st.theme, label: th.label, main: main, more: more, test: th.test, art: th.articles[0], ts: Date.now()}; A.save(); A.toast("Маршрут сохранён · +15 к пути");
      A.goal("navigator_route", {theme: st.theme});
      choices([["Собрать маршрут заново", function(){ st = {}; askTheme("Давайте заново. <b>Что сейчас ближе всего?</b>"); }]]);
    }
    function matchTheme(text){ var t = text.toLowerCase(), best = null, bs = 0; Object.keys(TH).forEach(function(k){ var s = 0; (TH[k].kw||[]).forEach(function(w){ if(t.indexOf(w) > -1) s++; }); if(s > bs){ bs = s; best = k; } }); return best; }
    function scripted(text){
      var k = matchTheme(text);
      if(/(плохо|не хочу жить|суицид|покончить|умереть|самоповрежд)/i.test(text)){ say("Мне важно, чтобы вы были в безопасности. Если вам сейчас очень тяжело — пожалуйста, позвоните <b>112</b> или на линию экстренной психологической помощи МЧС <b>+7 (495) 989-50-50</b> (круглосуточно, анонимно). Все контакты — <a href='" + R + "vazhno/#help'>здесь</a>."); return; }
      if(k){ st = {theme: k}; say("Похоже, это про тему «" + esc(TH[k].label) + "». Уточню пару моментов."); askLevel(); }
      else { say("Я пока не уверена, что правильно поняла. Выберите, что ближе:"); choices(Object.keys(TH).map(function(x){ return [TH[x].label, function(){ st = {theme: x}; askLevel(); }]; })); }
    }
    function askAI(text){
      var typing = say("Думаю", "bot"); typing.classList.add("typing"); history.pop();
      var ctl = window.AbortController ? new AbortController() : null, timer = setTimeout(function(){ if(ctl) ctl.abort(); }, +C.aiTimeoutMs || 12000), finished = false;
      function fail(){ if(finished) return; finished = true; clearTimeout(timer); typing.remove(); setMode(false); scripted(text); }
      fetch(EP, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({messages: (function(h){ while(h.length && h[0].role !== "user") h.shift(); return h; })(history.slice(-12)), page: A.page, mode: "navigator"}), signal: ctl ? ctl.signal : undefined})
        .then(function(r){ if(!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
        .then(function(j){
          if(finished) return;
          var reply = j && typeof j.reply === "string" ? j.reply.trim() : "";
          if(!reply) return fail();
          finished = true; clearTimeout(timer); typing.remove();
          var d = say(reply, "bot", true);
          if(Array.isArray(j.suggestions) && j.suggestions.length){
            var w = document.createElement("div"); w.className = "route";
            j.suggestions.slice(0, 5).forEach(function(s){ if(!s || !s.label) return; var a = document.createElement("a"); a.href = safeUrl(s.url); var sp = document.createElement("span"); sp.textContent = s.label; a.appendChild(sp); w.appendChild(a); });
            d.appendChild(w);
          }
          log.scrollTop = log.scrollHeight;
        })["catch"](fail);
    }
    form.addEventListener("submit", function(e){
      e.preventDefault(); var t = inp.value.trim(); if(!t) return; inp.value = ""; say(t, "me", true); opts.innerHTML = "";
      if(aiOn) askAI(t); else setTimeout(function(){ scripted(t); }, A.reduce ? 0 : 300);
    });
    if(A.S.route && TH[A.S.route.theme]) askTheme("С возвращением! Ваш прошлый маршрут — «" + esc(A.S.route.label) + "» (он в <a href='" + R + "moj-put/'>«Моём пути»</a>). <b>Что актуально сегодня?</b>");
    else askTheme();
  });

  /* ===================== ТЕСТЫ ===================== */
  $$("[data-test]").forEach(function(box){
    var t = TEST[box.dataset.test]; if(!t) return;
    var SC = VK.scale || ["Никогда","Редко","Иногда","Часто","Почти всегда"], ans = [], i = 0;
    function itemText(it){ return typeof it === "string" ? it : it[0]; }
    function render(){
      if(t.kind === "wheel") return wheel();
      var it = t.items[i], total = t.items.length;
      var o = t.kind === "type" ? it[1].map(function(x, j){ return '<button type="button" data-v="' + j + '">' + esc(x[0]) + '</button>'; }).join("")
                                : SC.map(function(x, j){ return '<button type="button" data-v="' + j + '">' + esc(x) + '</button>'; }).join("");
      box.innerHTML = '<div class="qprog" aria-hidden="true"><i style="width:' + (i/total*100) + '%"></i></div><span class="kick">Вопрос ' + (i+1) + ' из ' + total + '</span><p class="qtext">' + esc(itemText(it)) + '</p><div class="qopts">' + o + '</div><div class="qnav">' + (i ? '<button class="btn ghost sm" type="button" data-back>← Назад</button>' : '<span></span>') + '<span class="small muted">Отвечайте первым, что приходит в голову</span></div>';
      $$("[data-v]", box).forEach(function(b){ b.addEventListener("click", function(){ ans[i] = +b.dataset.v; i++; if(i >= total) result(); else render(); }); });
      var bk = $("[data-back]", box); if(bk) bk.addEventListener("click", function(){ i--; render(); });
      var f = $(".qopts button", box); if(f && i) f.focus();
    }
    function bars(map, names, max){ return '<div class="bars">' + Object.keys(names).map(function(k){ var v = map[k]||0; return '<div class="bar"><span>' + esc(names[k]) + '</span><i><b style="width:' + Math.round(v/max*100) + '%"></b></i><span>' + v + '</span></div>'; }).join("") + '</div>'; }
    function finish(title, text, arts, pk, extra){
      var p = VK.prods[pk], deep = VK.prods[t.deep];
      A.S.tests[t.slug] = {t: t.title, r: title, p: pk, ts: Date.now()}; var fresh = true; A.save(); A.toast("Результат сохранён в «Мой путь» · +20");
      A.goal("test_done", {test: t.slug});
      box.innerHTML = '<div class="res"><span class="kick">Ваш результат</span><h2>' + esc(title) + '</h2>' + (extra||"") + '<p>' + esc(text) + '</p>' +
        '<p class="small muted">Это не диагноз, а повод для самонаблюдения. Тест авторский, не клинический.</p>' +
        '<h3>Что почитать</h3><div class="route">' + arts.map(artLink).join("") + '</div>' +
        '<div class="glass box offer"><span class="kick">Следующий шаг · вживую с Мариной</span><h3>' + esc(p ? p.t : "") + '</h3><p class="small muted">' + esc(p ? (p.s || "") : "") + '</p><div class="btns">' + A.ctaHtml(pk) + (pk !== "diag" ? A.ctaHtml("diag", "Диагностика 30 мин · " + A.price("diagnostika"), "btn ghost") : "") + '</div>' +
        (deep && t.deep !== pk ? '<p class="small mt">Глубже: <a href="' + prodUrl(t.deep) + '">' + esc(deep.t) + '</a></p>' : "") + '</div>' +
        '<div class="btns"><button class="btn ghost sm" type="button" data-again>Пройти заново</button><a class="btn ghost sm" href="' + R + 'testy/">Другие тесты</a><a class="btn ghost sm" href="' + R + 'moj-put/">Мой путь</a></div></div>';
      A.initCta(box);
      $("[data-again]", box).addEventListener("click", function(){ ans = []; i = 0; render(); });
      box.scrollIntoView({behavior: A.reduce ? "auto" : "smooth", block: "start"});
      var cv = $("canvas.radar", box); if(cv) radar(cv, extraVals);
    }
    var extraVals = null;
    function result(){
      if(t.kind === "scale"){
        var s = ans.reduce(function(a, b){ return a + b; }, 0), max = t.items.length*4, band = t.bands.filter(function(b){ return s >= b[0] && s <= b[1]; })[0] || t.bands[t.bands.length-1];
        var idx = t.bands.indexOf(band), pk = idx === 0 ? (t.slug === "resurs" ? "klub" : t.step) : idx === 1 ? t.step : (t.slug === "resurs" ? "individ" : t.deep);
        if(idx === 2 && t.slug !== "resurs" && t.deep.indexOf("modul") === 0) pk = t.step;
        var ex = '<div class="meter" role="img" aria-label="' + s + ' из ' + max + '"><b style="left:calc(' + (s/max*100) + '% - 2px)"></b></div><p class="small muted">' + s + ' из ' + max + ' баллов</p>';
        if(t.slug === "resurs" && idx === 2) ex += '<p class="note">Если усталость, бессонница или подавленность держатся дольше двух недель — обратитесь к врачу. Это не повод для паники, а забота о себе. <a href="' + R + 'vazhno/">Подробнее</a></p>';
        finish(band[2], band[3], t.articles.slice(0, 3), pk, ex);
      } else if(t.kind === "type"){
        var cnt = {}; ans.forEach(function(a, j){ var k = t.items[j][1][a][1]; cnt[k] = (cnt[k]||0) + 1; });
        var top = Object.keys(t.types).sort(function(a, b){ return (cnt[b]||0) - (cnt[a]||0); })[0], r = t.results[top];
        finish(r[0], r[1], r[2], r[3], bars(cnt, t.types, t.items.length));
      } else if(t.kind === "multi"){
        var sc = {}; ans.forEach(function(a, j){ var k = t.items[j][1]; sc[k] = (sc[k]||0) + a; });
        var top2 = Object.keys(t.types).sort(function(a, b){ return (sc[b]||0) - (sc[a]||0); })[0], r2 = t.results[top2];
        var per = t.items.filter(function(x){ return x[1] === top2; }).length*4;
        finish(r2[0], r2[1], r2[2], r2[3], bars(sc, t.types, per));
      } else if(t.kind === "perf"){
        var a1 = 0, f1 = 0, nst = 0, nf = 0; ans.forEach(function(a, j){ if(t.items[j][1] === "st"){ a1 += a; nst++; } else { f1 += a; nf++; } });
        var hiS = a1 >= nst*2.4, hiF = f1 >= nf*2.4, k = hiS && !hiF ? "friend" : hiS && hiF ? "guard" : hiF ? "fear" : "calm", r3 = t.results[k];
        finish(r3[0], r3[1], r3[2], r3[3], bars({st: a1, fear: f1}, {st: "Высокие стандарты", fear: "Страх ошибки"}, Math.max(nst, nf)*4));
      }
    }
    function wheel(){
      var sp = t.spheres, v = sp.map(function(){ return 5; });
      box.innerHTML = '<span class="kick">Оцените каждую сферу от 1 до 10</span><div class="wheelrow"><div class="slid">' + sp.map(function(s, j){ return '<label for="w' + j + '">' + esc(s[1]) + ': <b data-wv="' + j + '">5</b></label><input id="w' + j + '" type="range" min="1" max="10" value="5" data-w="' + j + '">'; }).join("") + '</div><canvas class="radar" width="440" height="440" role="img" aria-label="Диаграмма колеса баланса"></canvas></div><div class="btns"><button class="btn" type="button" data-wgo>Показать разбор</button></div>';
      var cv = $("canvas", box);
      $$("[data-w]", box).forEach(function(r){ r.addEventListener("input", function(){ v[+r.dataset.w] = +r.value; $('[data-wv="' + r.dataset.w + '"]', box).textContent = r.value; radar(cv, v); }); });
      radar(cv, v);
      $("[data-wgo]", box).addEventListener("click", function(){
        var lo = 0; v.forEach(function(x, j){ if(x < v[lo]) lo = j; });
        var s = sp[lo], thKey = {opora: "kontrol"}[s[0]] || s[0], th = (VK.themes||{})[thKey] || {articles: t.articles};
        extraVals = v.slice();
        var avg = (v.reduce(function(a, b){ return a + b; }, 0)/v.length).toFixed(1);
        finish("Точка роста: «" + s[1] + "»", "Средняя оценка вашего колеса — " + avg + " из 10. Самая просевшая сфера сейчас — «" + s[1] + "» (" + v[lo] + "/10). Колесо «едет» неровно, когда одна спица короче других, поэтому начинать стоит отсюда. Это субъективная оценка на сегодня — повторите через месяц и сравните.", th.articles.slice(0, 3), s[2],
          '<canvas class="radar" width="440" height="440" role="img" aria-label="Ваше колесо баланса"></canvas>');
      });
    }
    function radar(cv, v){
      var x = cv.getContext("2d"), W = cv.width, c = W/2, R0 = W*0.36, n = v.length, names = t.spheres.map(function(s){ return s[1]; });
      x.clearRect(0, 0, W, W); x.font = "600 13px Manrope, sans-serif"; x.textAlign = "center";
      for(var g = 1; g <= 5; g++){ x.beginPath(); for(var j = 0; j <= n; j++){ var a = -Math.PI/2 + j*2*Math.PI/n, r = R0*g/5; x[j ? "lineTo" : "moveTo"](c + r*Math.cos(a), c + r*Math.sin(a)); } x.strokeStyle = "rgba(255,255,255,.12)"; x.stroke(); }
      var grd = x.createLinearGradient(0, 0, W, W); grd.addColorStop(0, "rgba(124,247,255,.55)"); grd.addColorStop(.5, "rgba(155,123,255,.5)"); grd.addColorStop(1, "rgba(255,107,214,.55)");
      x.beginPath(); v.forEach(function(val, j){ var a = -Math.PI/2 + j*2*Math.PI/n, r = R0*val/10; x[j ? "lineTo" : "moveTo"](c + r*Math.cos(a), c + r*Math.sin(a)); }); x.closePath(); x.fillStyle = grd; x.fill(); x.strokeStyle = "#7cf7ff"; x.lineWidth = 2; x.stroke();
      v.forEach(function(val, j){ var a = -Math.PI/2 + j*2*Math.PI/n, r = R0*val/10; x.fillStyle = "#fff"; x.beginPath(); x.arc(c + r*Math.cos(a), c + r*Math.sin(a), 4, 0, 6.3); x.fill();
        var lx = c + (R0 + 30)*Math.cos(a), ly = c + (R0 + 26)*Math.sin(a); x.fillStyle = "#d9d3f5"; var w = names[j].split(" "); if(w.length > 2){ x.fillText(w.slice(0, 2).join(" "), lx, ly - 7); x.fillText(w.slice(2).join(" "), lx, ly + 9); } else x.fillText(names[j], lx, ly + 4); });
    }
    render();
  });

  /* ===================== КАРТА ДНЯ ===================== */
  function rng(seed){ var s = 0; for(var i = 0; i < seed.length; i++) s = (s*31 + seed.charCodeAt(i)) >>> 0; return function(){ s = (s + 0x6D2B79F5) >>> 0; var t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0)/4294967296; }; }
  $$("[data-cardday]").forEach(function(box){
    var cv = $("canvas", box), x = cv.getContext("2d"), today = new Date(), dstr = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate(), off = 0;
    var note = $("[data-cd-note]", box), ok = $("[data-cd-ok]", box);
    function draw(){
      var r = rng(dstr + ":" + off), W = cv.width, H = cv.height, hues = [186, 258, 316, 45, 150], h1 = hues[Math.floor(r()*5)], h2 = hues[Math.floor(r()*5)];
      var g = x.createLinearGradient(0, 0, W, H); g.addColorStop(0, "hsl(" + h1 + ",60%,12%)"); g.addColorStop(1, "hsl(" + h2 + ",70%,22%)"); x.fillStyle = g; x.fillRect(0, 0, W, H);
      for(var i = 0; i < 160; i++){ x.fillStyle = "rgba(255,255,255," + (r()*.7) + ")"; x.beginPath(); x.arc(r()*W, r()*H, r()*1.6, 0, 6.3); x.fill(); }
      x.globalCompositeOperation = "lighter";
      for(var k = 0; k < 7; k++){ var cx = W*(.2 + r()*.6), cy = H*(.2 + r()*.6), rad = 60 + r()*220, gr = x.createRadialGradient(cx, cy, 0, cx, cy, rad), hh = hues[Math.floor(r()*5)];
        gr.addColorStop(0, "hsla(" + hh + ",95%,65%,.55)"); gr.addColorStop(1, "hsla(" + hh + ",95%,50%,0)"); x.fillStyle = gr; x.beginPath(); x.arc(cx, cy, rad, 0, 6.3); x.fill(); }
      for(var L = 0; L < 5; L++){ x.strokeStyle = "hsla(" + hues[Math.floor(r()*5)] + ",90%,75%,.5)"; x.lineWidth = 1 + r()*2.5; x.beginPath(); var y0 = r()*H; x.moveTo(0, y0);
        x.bezierCurveTo(W*.3, r()*H, W*.7, r()*H, W, r()*H); x.stroke(); }
      x.globalCompositeOperation = "source-over";
      var sym = Math.floor(r()*3); x.strokeStyle = "rgba(255,255,255,.85)"; x.lineWidth = 2.5; x.beginPath();
      if(sym === 0){ x.arc(W/2, H/2, 90, 0, 6.3); } else if(sym === 1){ for(var j = 0; j <= 3; j++){ var a = -Math.PI/2 + j*2*Math.PI/3; x[j ? "lineTo" : "moveTo"](W/2 + 100*Math.cos(a), H/2 + 100*Math.sin(a)); } } else { for(var q = 0; q < 6; q++){ var a2 = q*Math.PI/3; x.moveTo(W/2, H/2); x.lineTo(W/2 + 110*Math.cos(a2), H/2 + 110*Math.sin(a2)); } }
      x.stroke();
      x.strokeStyle = "rgba(255,255,255,.35)"; x.lineWidth = 2; x.strokeRect(18, 18, W - 36, H - 36);
      var wi = Math.floor(r()*VK.card.w.length), qi = Math.floor(r()*VK.card.q.length), word = VK.card.w[wi];
      x.fillStyle = "#fff"; x.font = "700 40px Unbounded, Manrope, sans-serif"; x.textAlign = "center"; x.fillText(word.toUpperCase(), W/2, H - 70);
      $("[data-cd-word]", box).textContent = word; $("[data-cd-q]", box).textContent = VK.card.q[qi];
      $("[data-cd-date]", box).textContent = (off ? "Дополнительная карта · " : "Карта дня · ") + today.toLocaleDateString("ru-RU", {day: "numeric", month: "long"});
      try{ note.value = localStorage.getItem("vk_card_" + dstr + "_" + off) || ""; }catch(e){}
      ok.textContent = "";
    }
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(draw); else draw();
    $("[data-cd-save]", box).addEventListener("click", function(){ try{ localStorage.setItem("vk_card_" + dstr + "_" + off, note.value); }catch(e){} ok.textContent = "Сохранено в этом браузере."; A.award("gifts", "card"); });
    $("[data-cd-more]", box).addEventListener("click", function(){ off++; draw(); A.award("gifts", "card"); });
  });

  /* ===================== МИНИ-ЛИЛА ===================== */
  $$("[data-lila]").forEach(function(box){
    var cells = VK.lila.cells, J = VK.lila.jumps, N = cells.length, pos = 0, tries = 0, path = [], over = false;
    var rows = [], order = [];
    for(var r = N/6 - 1; r >= 0; r--){ var row = []; for(var c = 0; c < 6; c++) row.push(r*6 + c + 1); if(r % 2) row.reverse(); order = order.concat(row); }
    box.innerHTML = '<div class="board glass" role="grid" aria-label="Поле игры: 36 клеток">' + order.map(function(n){ var cl = cells[n-1], j = J[String(n)], k = j ? (j > n ? " up" : " down") : "";
      return '<div class="cell' + k + '" data-n="' + n + '" title="' + esc(n + ". " + cl[1] + (j ? " → " + j : "")) + '"><span class="cn">' + n + '</span><span>' + esc(cl[1]) + '</span></div>'; }).join("") + '</div>' +
      '<div class="lpanel glass"><label class="small muted" for="lq">Ваш запрос на игру (необязательно)</label><input id="lq" type="text" maxlength="140" placeholder="Например: что мешает мне поднять цену?" style="padding:12px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.15);background:rgba(0,0,0,.25);color:#fff;font:500 15px Manrope,sans-serif">' +
      '<div style="display:flex;gap:16px;align-items:center"><div class="die" aria-live="polite" data-die>?</div><div><button class="btn" type="button" data-roll>Бросить кубик</button><p class="small muted" data-hint style="margin:8px 0 0">Чтобы войти в игру, нужна шестёрка.</p></div></div>' +
      '<div data-cellinfo><span class="kick">Старт</span><h3>Перед входом</h3><p class="muted">Сформулируйте запрос. Каждая клетка — это вопрос к себе: задержитесь на нём хотя бы на один вдох.</p></div>' +
      '<ol class="llog" data-log></ol><div data-fin></div></div>';
    var die = $("[data-die]", box), btn = $("[data-roll]", box), hint = $("[data-hint]", box), info = $("[data-cellinfo]", box), lg = $("[data-log]", box);
    function log(t){ var li = document.createElement("li"); li.textContent = t; lg.insertBefore(li, lg.firstChild); }
    function mark(){ $$(".cell", box).forEach(function(el){ var n = +el.dataset.n; el.classList.toggle("here", n === pos); el.classList.toggle("visited", path.indexOf(n) > -1); }); }
    function show(n, extra){ var cl = cells[n-1]; info.innerHTML = '<span class="kick">Клетка ' + n + (extra ? " · " + esc(extra) : "") + '</span><h3>' + esc(cl[1]) + '</h3><p class="muted">' + esc(cl[2]) + '</p><p><b>Вопрос:</b> ' + esc(cl[3]) + '</p>'; }
    btn.addEventListener("click", function(){
      if(over) return;
      var d = 1 + Math.floor(Math.random()*6); die.textContent = d; die.classList.remove("roll"); void die.offsetWidth; die.classList.add("roll");
      if(pos === 0){
        tries++;
        if(d === 6 || tries >= 3){ pos = 1; path.push(1); log((d === 6 ? "Выпала 6 — " : "Третья попытка — мягкое правило: ") + "вы вошли в игру."); hint.textContent = "Бросайте дальше. Стрелы поднимают, змеи возвращают."; show(1, "вход"); mark(); }
        else { log("Выпало " + d + ". Нужна 6 (попытка " + tries + " из 3)."); hint.textContent = "Ещё попытка. После третьей войдёте в любом случае."; }
        return;
      }
      var to = Math.min(N, pos + d), extra = ""; path.push(to); log("Выпало " + d + " → клетка " + to + " «" + cells[to-1][1] + "»");
      var j = J[String(to)];
      if(j){ extra = j > to ? "стрела ↑ с " + to : "змея ↓ с " + to; log((j > to ? "Стрела! " : "Змея… ") + to + " → " + j + " «" + cells[j-1][1] + "»"); to = j; path.push(to); }
      pos = to; show(pos, extra); mark();
      if(pos >= N){ over = true; btn.disabled = true; hint.textContent = "Игра завершена.";
        A.award("gifts", "lila"); A.goal("minilila_done");
        var q = $("#lq", box).value.trim(), uniq = path.filter(function(v, i2, a){ return a.indexOf(v) === i2; });
        var f = $("[data-fin]", box); f.innerHTML = '<div class="glass box offer"><span class="kick">Вы дошли до клетки ' + N + '</span><h3>Ваш путь: ' + uniq.length + ' клеток' + (q ? ' по запросу «' + esc(q) + '»' : '') + '</h3><p class="small muted">Запишите 1–2 клетки, которые отозвались сильнее всего, и один шаг на 24 часа. В полной игре «Лила» с Мариной (72 клетки, 4 часа, до 4 игроков) запрос разбирается глубоко и с обратной связью ведущей.</p><div class="btns">' + A.ctaHtml("lila") + '<a class="btn ghost sm" href="' + R + 'lila/">О полной игре</a><button class="btn ghost sm" type="button" data-again>Сыграть ещё</button></div></div>';
        A.initCta(f); $("[data-again]", f).addEventListener("click", function(){ pos = 0; tries = 0; path = []; over = false; btn.disabled = false; lg.innerHTML = ""; f.innerHTML = ""; die.textContent = "?"; hint.textContent = "Чтобы войти в игру, нужна шестёрка."; mark(); });
      }
    });
  });

  /* ===================== ДЫХАНИЕ ===================== */
  $$("[data-breath]").forEach(function(box){
    var c = $("[data-b-c]", box), tx = $("[data-b-txt]", box), left = $("[data-b-left]", box), timer = 0, end = 0, run = false;
    var NAMES = ["Вдох", "Пауза", "Выдох", "Пауза"];
    function stop(msg){ run = false; clearTimeout(timer); c.style.transition = ""; c.style.transform = "scale(.6)"; tx.textContent = msg || "Готовы?"; left.textContent = ""; }
    function phase(seq, k){
      if(!run) return; if(Date.now() >= end){ stop("Готово. Как вы сейчас?"); A.award("gifts", "breath"); return; }
      var s = seq[k]; if(!s) return phase(seq, (k + 1) % 4);
      tx.textContent = NAMES[k] + " · " + s;
      if(!A.reduce){ c.style.transition = "transform " + s + "s ease-in-out"; if(k === 0) c.style.transform = "scale(1)"; if(k === 2) c.style.transform = "scale(.6)"; }
      var cnt = s, tick = function(){ cnt--; if(cnt > 0 && run){ tx.textContent = NAMES[k] + " · " + cnt; timer = setTimeout(tick, 1000); } else timer = setTimeout(function(){ phase(seq, (k + 1) % 4); }, 0); };
      left.textContent = "Осталось ~" + Math.max(0, Math.ceil((end - Date.now())/60000)) + " мин";
      timer = setTimeout(tick, 1000);
    }
    $("[data-b-start]", box).addEventListener("click", function(){ stop(); run = true; end = Date.now() + 60000*(+$("[data-b-min]", box).value); phase($("[data-b-mode]", box).value.split(",").map(Number), 0); });
    $("[data-b-stop]", box).addEventListener("click", function(){ stop(); });
  });

  /* ===================== ЧЕЛЛЕНДЖ ===================== */
  var chs = $$("[data-ch]");
  if(chs.length){
    var barEl = $("[data-ch-bar]"), stat = $("[data-ch-stat]"), doneEl = $("[data-ch-done]");
    function upd(){ var n = chs.filter(function(c){ return c.checked; }).length; barEl.style.width = (n/chs.length*100) + "%"; stat.textContent = "Пройдено дней: " + n + " из " + chs.length; doneEl.classList.toggle("hidden", n < chs.length);
      chs.forEach(function(c){ c.closest(".cday").classList.toggle("done", c.checked); }); }
    chs.forEach(function(c){ c.checked = !!A.S.ch[c.dataset.ch]; c.addEventListener("change", function(){ if(c.checked) A.award("ch", c.dataset.ch); else { delete A.S.ch[c.dataset.ch]; A.save(); } upd(); }); });
    upd();
  }

  /* ===================== МОЙ ПУТЬ ===================== */
  $$("[data-mypath]").forEach(function(box){
    function paint(){
      var S = A.S, L = A.level(), na = Object.keys(S.arts).length, nt = Object.keys(S.tests).length, nd = Object.keys(S.done).length, nc = Object.keys(S.ch).length;
      var B = [["📖", "Первая статья", na >= 1], ["📚", "5 статей", na >= 5], ["🎓", "Энциклопедист: 15 статей", na >= 15], ["🧭", "Маршрут навигатора", !!S.route], ["🔍", "Первый тест", nt >= 1], ["🪞", "Самонаблюдатель: 4 теста", nt >= 4],
               ["🛠", "3 практики", nd >= 3], ["🃏", "Карта дня", !!S.gifts.card], ["🎲", "Мини-Лила пройдена", !!S.gifts.lila], ["🌬", "Сессия дыхания", !!S.gifts.breath], ["📄", "PDF скачан", !!S.gifts.pdf], ["🔥", "Челлендж 7 дней", nc >= 7]];
      var res = Object.keys(S.tests).map(function(k){ var x = S.tests[k], p = VK.prods[x.p]; return '<div class="glass card"><span class="kick">' + esc(x.t) + '</span><h3>' + esc(x.r) + '</h3><div class="btns"><a class="btn ghost sm" href="' + R + 'testy/' + k + '/">Пройти снова</a>' + (p ? A.ctaHtml(x.p, p.t + " · " + A.price(p.code, p.g), "btn sm") : "") + '</div></div>'; }).join("");
      var next;
      if(!S.route && !nt) next = ['Начните с навигатора — он соберёт маршрут за минуту.', '<a class="btn" href="' + R + 'navigator/">Открыть навигатор</a>'];
      else if(S.route && !S.tests[S.route.test]) next = ['По вашему маршруту «' + esc(S.route.label) + '» следующий шаг — тест.', '<a class="btn" href="' + R + 'testy/' + S.route.test + '/">Пройти тест</a>'];
      else { var pk = (S.route && S.route.main) || "diag"; next = ['Вы много узнали сами. Следующий шаг — живая работа с Мариной: увидеть, что стоит за вашей ситуацией.', A.ctaHtml(pk) + (pk !== "diag" ? A.ctaHtml("diag", "Диагностика · " + A.price("diagnostika"), "btn ghost") : "")]; }
      box.innerHTML = '<div class="mp-top glass"><div class="ring-lvl" style="--p:' + L.pct + '"><b>' + L.n + '</b></div><div><span class="kick">Уровень ' + L.n + ' из ' + A.LEVELS.length + '</span><h2>' + esc(L.name) + '</h2><p class="muted">' + L.pts + ' очков пути. Статья +10, тест +20, практика +15, подарок +10, день челленджа +10.</p></div></div>' +
        '<div class="stats"><div class="glass stat"><b>' + na + '</b>статей из ' + VK.nArts + '</div><div class="glass stat"><b>' + nt + '</b>тестов из ' + (VK.tests||[]).length + '</div><div class="glass stat"><b>' + nd + '</b>практик</div><div class="glass stat"><b>' + nc + '/7</b>дней челленджа</div></div>' +
        '<div class="glass box offer"><span class="kick">Ваш следующий шаг</span><p>' + next[0] + '</p><div class="btns">' + next[1] + '</div></div>' +
        (S.route ? '<div class="glass box"><span class="kick">Маршрут навигатора</span><h3>' + esc(S.route.label) + '</h3><div class="route">' + artLink(S.route.art) + '<a href="' + R + 'testy/' + S.route.test + '/"><span>Тест по теме<small>Бесплатно</small></span></a><a href="' + prodUrl(S.route.main) + '"><span>' + esc((VK.prods[S.route.main]||{}).t || "") + '<small>Живой шаг</small></span></a></div></div>' : "") +
        '<h2 class="mt">Награды</h2><div class="badges">' + B.map(function(b){ return '<div class="badge' + (b[2] ? " on" : "") + '"><span class="emo">' + b[0] + '</span>' + esc(b[1]) + '</div>'; }).join("") + '</div>' +
        (res ? '<h2 class="mt">Результаты тестов</h2><div class="grid g2">' + res + '</div>' : '') +
        '<p class="small muted mt">Всё хранится только в этом браузере. <button class="btn ghost sm" type="button" data-reset>Сбросить прогресс</button></p>';
      A.initCta(box);
      $("[data-reset]", box).addEventListener("click", function(){ if(confirm("Удалить весь прогресс, результаты и маршрут из этого браузера?")){ ["arts","tests","done","gifts","ch"].forEach(function(k){ A.S[k] = {}; }); delete A.S.route; A.save(); paint(); } });
    }
    paint();
  });
})();
