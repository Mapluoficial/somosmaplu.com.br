// Cotações ao vivo (AwesomeAPI, gratuita). Atualiza a cada 60 s.
(function () {
  var fmt = function (v, k) {
    var n = parseFloat(v);
    return k === 'BTCBRL'
      ? 'R$ ' + Math.round(n / 1000).toLocaleString('pt-BR') + ' mil'
      : 'R$ ' + n.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
  function atualiza() {
    fetch('https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL')
      .then(function (r) { return r.json(); })
      .then(function (j) {
        document.querySelectorAll('.tk').forEach(function (el) {
          var k = el.getAttribute('data-k'), q = j[k];
          if (!q) return;
          var p = parseFloat(q.pctChange);
          el.querySelector('b').textContent = fmt(q.bid, k);
          var i = el.querySelector('i') || el.appendChild(document.createElement('i'));
          i.className = p >= 0 ? 'up' : 'dn';
          i.textContent = (p >= 0 ? '▲' : '▼') + Math.abs(p).toFixed(2).replace('.', ',') + '%';
        });
      })
      .catch(function () {});
  }
  atualiza();
  setInterval(atualiza, 60000);
})();
