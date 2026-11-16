// ==============================================================================
// ALMİNA TAROT - CANLI YAYIN MOTORU (STABİL 4K GÖRSEL, SEANS MÜZİĞİ & 3D KARTLAR)
// ==============================================================================

const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const socketUrl = `${wsProtocol}//${window.location.host}/ws`;
let ws;
let isCurrentlyReading = false;
let idleResetTimer = null;

const elements = {
  userFullName: document.getElementById('userFullName'),
  badgePill: document.getElementById('badgePill'),
  zodiacPillLine: document.getElementById('zodiacPillLine'),
  zodiacBadge: document.getElementById('zodiacBadge'),
  userSubquestion: document.getElementById('userSubquestion'),
  cardStage: document.getElementById('cardStage'),
  deckBox: document.getElementById('deckShuffleBox'),
  shuffleBanner: document.getElementById('shuffleBanner'),
  ttsAudio: document.getElementById('ttsAudio'),
  bgAmbientAudio: document.getElementById('bgAmbientAudio')
};

// 1. MİSTİK SEANS FON MÜZİĞİ (KISIK SESLE SÜREKLİ DÖNGÜ)
function startAmbientMusic() {
  if (elements.bgAmbientAudio) {
    elements.bgAmbientAudio.volume = 0.12; // Kısık, sakin tını
    elements.bgAmbientAudio.play().catch(() => {});
  }
}

// 2. KART KARIŞTIRMA SES EFEKTİ
function playShuffleAudio() {
  try {
    const audio = new Audio('/audio/shuffle.wav');
    audio.volume = 0.55;
    audio.play().catch(() => {});
  } catch (e) {}
}

// 3. WEBSOCKET BAĞLANTISI
function connectWebSocket() {
  ws = new WebSocket(socketUrl);

  ws.onopen = () => {
    console.log('[WebSocket] Canlı yayın ekranına bağlanıldı.');
  };

  ws.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.type === 'NEW_READING') {
        renderReading(payload.data);
      } else if (payload.type === 'WAIT_FOR_QUESTION') {
        renderWaitForQuestion(payload.data);
      } else if (payload.type === 'IDLE') {
        renderIdle();
      }
    } catch (e) {
      console.error('[WebSocket] Hata:', e);
    }
  };

  ws.onclose = () => {
    setTimeout(connectWebSocket, 1500);
  };
}

// 4. SORU BEKLEME BİLDİRİMİ (KART KARIŞTIRMADAN SADECE ANONS)
function renderWaitForQuestion(data) {
  isCurrentlyReading = true;
  if (idleResetTimer) {
    clearTimeout(idleResetTimer);
    idleResetTimer = null;
  }

  startAmbientMusic();

  const { username, question, badge, audio_url } = data;
  if (elements.userFullName) elements.userFullName.textContent = username || 'Canlı İzleyici';
  if (elements.userSubquestion) elements.userSubquestion.textContent = question || '✦ Niyetini chatten bekliyorum... ✦';
  if (elements.badgePill) elements.badgePill.textContent = badge || 'Soru Bekleniyor';
  if (elements.zodiacPillLine) elements.zodiacPillLine.style.display = 'none';

  if (audio_url && elements.ttsAudio) {
    elements.ttsAudio.src = audio_url;
    elements.ttsAudio.play().catch(() => {});
  }
}

// 5. YENİ AÇILIM VE 3D KART KARIŞTIRMA/AÇMA
function renderReading(data) {
  isCurrentlyReading = true;
  if (idleResetTimer) {
    clearTimeout(idleResetTimer);
    idleResetTimer = null;
  }

  const { username, question, tier, badge, zodiac_badge, cards, audio_url } = data;

  startAmbientMusic();

  // 1. İzleyici Bilgileri ve Rozet (Hediye/jeton adı ASLA geçmez)
  if (elements.userFullName) elements.userFullName.textContent = username || 'Canlı İzleyici';
  if (elements.userSubquestion) elements.userSubquestion.textContent = question ? `"${question}"` : `"Detaylı Tek Kart"`;
  if (elements.badgePill) elements.badgePill.textContent = badge || 'Detaylı Tek Kart';

  // Hediye Vitrini: Bakılan açılıma göre ilgili kutucuğu kilitli ışıltıyla vurgula
  highlightGiftTier(badge || tier);

  // Burç & Doğum Tarihi Rozeti
  if (zodiac_badge && elements.zodiacBadge && elements.zodiacPillLine) {
    elements.zodiacBadge.textContent = zodiac_badge;
    elements.zodiacPillLine.style.display = 'flex';
  } else if (elements.zodiacPillLine) {
    elements.zodiacPillLine.style.display = 'none';
  }

  // Eğer kart listesi yoksa veya boşsa sadece sesi oynat
  if (!cards || cards.length === 0) {
    if (audio_url && elements.ttsAudio) {
      elements.ttsAudio.src = audio_url;
      elements.ttsAudio.play().catch(() => {});
    }
    return;
  }

  // 2. KARTLARI KARIŞTIRMA ANİMASYONUNU BAŞLAT
  if (elements.cardStage) {
    elements.cardStage.innerHTML = '';
    elements.cardStage.className = `tarot-card-stage card-count-${cards.length}`;
  }

  if (elements.shuffleBanner) elements.shuffleBanner.classList.add('visible');
  if (elements.deckBox) elements.deckBox.classList.add('active', 'is-shuffling');
  playShuffleAudio();

  // 1.25 saniye masada karıştır, ardından kartları masaya dağıt
  setTimeout(() => {
    if (elements.deckBox) elements.deckBox.classList.remove('active', 'is-shuffling');
    if (elements.shuffleBanner) elements.shuffleBanner.classList.remove('visible');

    let labels = ['Cevap'];
    if (cards.length === 3) {
      labels = ['Geçmiş', 'Şimdi', 'Gelecek'];
    } else if (cards.length === 4) {
      labels = ['Aşk', 'Kariyer', 'Maddiyat', 'Gelecek'];
    } else if (cards.length === 5) {
      labels = ['Senin Enerjin', 'Aklındaki Kişi', 'Gizli Hisler', 'Blokajlar', 'Net Sonuç'];
    } else if (cards.length >= 6) {
      labels = ['Kadersel Sınav', 'Ruh Bağı', 'Görünmeyen Güç', 'Yakın Gelecek', 'Kader Çarkı', 'İlahi Mesaj'];
    }

    cards.forEach((card, idx) => {
      const cardWrap = document.createElement('div');
      cardWrap.className = 'card-wrapper card-deal-anim';
      cardWrap.style.animationDelay = `${idx * 0.18}s`;

      const imgSrc = card.image || 'cards/Cups04.jpg';
      const label = labels[idx] || 'Cevap';

      cardWrap.innerHTML = `
        <div class="tarot-card-frame">
          <div class="card-3d-flipper" id="flipper-${idx}">
            <div class="card-face card-back-face">
              <img src="cards/card_back.jpg" alt="Tarot Arka" class="tarot-img">
            </div>
            <div class="card-face card-front-face">
              <img src="${imgSrc}" alt="${card.name_tr}" class="tarot-img">
            </div>
          </div>
        </div>
        <div class="card-caption">
          <div class="caption-label">${label}</div>
          <div class="caption-name">${card.name_tr}</div>
        </div>
      `;

      elements.cardStage.appendChild(cardWrap);

      // Kartları masada 3D olarak sırayla çevir (Flip)
      setTimeout(() => {
        const flipper = document.getElementById(`flipper-${idx}`);
        if (flipper) flipper.classList.add('flipped');
      }, 350 + idx * 280);
    });

    // 3. Kartlar masaya açıldıktan sonra ses başlasın
    setTimeout(() => {
      if (audio_url && elements.ttsAudio) {
        elements.ttsAudio.src = audio_url;
        elements.ttsAudio.play().catch(e => {
          console.warn('Ses otomatik oynatma izni:', e);
        });
      }
    }, 550);

  }, 1250);
}

// 6. BAKIM BİTİNCE SAHNEYİ TEMİZLEME VE BEKLEME DURUMU
function renderIdle() {
  isCurrentlyReading = false;
  if (elements.cardStage) {
    elements.cardStage.classList.remove('is-reading');
    const wrappers = elements.cardStage.querySelectorAll('.card-wrapper');
    wrappers.forEach(w => w.classList.add('fading-out'));
  }

  // 1 saniye sonra masadaki eski kartları temizle ve genel yayın moduna dön
  if (idleResetTimer) clearTimeout(idleResetTimer);
  idleResetTimer = setTimeout(() => {
    if (!isCurrentlyReading) {
      if (elements.cardStage) elements.cardStage.innerHTML = '';
      if (elements.userFullName) elements.userFullName.textContent = 'Canlı Yayın';
      if (elements.userSubquestion) elements.userSubquestion.textContent = '✦ Chatten niyetinizi ve sorularınızı yazabilirsiniz ✦';
      if (elements.badgePill) elements.badgePill.textContent = 'Almina Tarot';
      if (elements.zodiacPillLine) elements.zodiacPillLine.style.display = 'none';
      startGiftShowcaseCycle();
    }
  }, 1000);
}

// ==============================================================================
// 7. DOĞAL İNSAN RİTMİNDE AĞIZ VE DUDAK ANİMASYONU (LIP-SYNC)
// ==============================================================================
let mouthTimer = null;

function startLipSync() {
  stopLipSync();
  const midEl = document.getElementById('bgTalkMid');
  const openEl = document.getElementById('bgTalkOpen');
  if (!midEl || !openEl) return;

  const pattern = [
    { mid: 1, open: 0, ms: 90 },
    { mid: 0, open: 1, ms: 140 },
    { mid: 1, open: 0, ms: 80 },
    { mid: 0, open: 0, ms: 110 },
    { mid: 1, open: 0, ms: 85 },
    { mid: 0, open: 1, ms: 160 },
    { mid: 0, open: 0, ms: 130 }
  ];

  let idx = 0;
  function animate() {
    if (elements.ttsAudio && !elements.ttsAudio.paused && !elements.ttsAudio.ended) {
      const step = pattern[idx];
      midEl.style.opacity = step.mid;
      openEl.style.opacity = step.open;
      idx = (idx + 1) % pattern.length;
      const jitter = Math.floor(Math.random() * 35) - 15;
      mouthTimer = setTimeout(animate, Math.max(60, step.ms + jitter));
    } else {
      stopLipSync();
    }
  }
  animate();
}

function stopLipSync() {
  if (mouthTimer) {
    clearTimeout(mouthTimer);
    mouthTimer = null;
  }
  const midEl = document.getElementById('bgTalkMid');
  const openEl = document.getElementById('bgTalkOpen');
  if (midEl) midEl.style.opacity = 0;
  if (openEl) openEl.style.opacity = 0;
}

// ==============================================================================
// 7.1 DOĞAL İNSAN GÖZ KIRPMA ANİMASYONU (BLINKING)
// ==============================================================================
let blinkTimeout = null;

function startBlinking() {
  const blinkEl = document.getElementById('bgBlink');
  if (!blinkEl) return;

  function scheduleNextBlink() {
    // 2.8 ile 5.5 saniye arasında doğal rastgele kırpma aralığı
    const delay = Math.floor(Math.random() * 2700) + 2800;
    blinkTimeout = setTimeout(() => {
      blinkEl.style.opacity = '1';
      setTimeout(() => {
        blinkEl.style.opacity = '0';
        // İnsanlarda %20 oranında peş peşe çift kırpma (micro-double blink)
        if (Math.random() < 0.22) {
          setTimeout(() => {
            blinkEl.style.opacity = '1';
            setTimeout(() => {
              blinkEl.style.opacity = '0';
              scheduleNextBlink();
            }, 100);
          }, 130);
        } else {
          scheduleNextBlink();
        }
      }, 130);
    }, delay);
  }

  scheduleNextBlink();
}

// 8. SES DİNLİYİCİLERİ VE ANLIK BİTİŞ BİLDİRİMİ
window.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();
  startAmbientMusic();
  startBlinking();
  startGiftShowcaseCycle();

  if (elements.ttsAudio) {
    elements.ttsAudio.addEventListener('play', () => {
      if (elements.cardStage) elements.cardStage.classList.add('is-reading');
      startLipSync();
    });

    elements.ttsAudio.addEventListener('pause', () => {
      if (elements.cardStage) elements.cardStage.classList.remove('is-reading');
      stopLipSync();
    });

    elements.ttsAudio.addEventListener('ended', () => {
      if (elements.cardStage) elements.cardStage.classList.remove('is-reading');
      stopLipSync();
      // BACKEND'E ANINDA BİTTİ BİLDİRİMİ GÖNDER (0ms GECİKME)
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'READING_FINISHED' }));
      }
    });
  }

  // İlk tıklamayla ses kısıtlamalarını kaldır ve fon müziğini başlat
  document.addEventListener('click', () => {
    startAmbientMusic();
    if (elements.ttsAudio) elements.ttsAudio.play().catch(() => {});
  }, { once: true });
});

// ==============================================================================
// 9. MOBİL TAM EKRAN VE PWA YÜKLEME KONTROLLERİ
// ==============================================================================
function toggleFullScreen() {
  const elem = document.documentElement;
  if (!document.fullscreenElement && !document.webkitFullscreenElement) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen().catch(() => {});
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen().catch(() => {});
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
}

function toggleInstallGuide() {
  const modal = document.getElementById('installGuideModal');
  if (modal) {
    modal.classList.toggle('open');
  }
}

// Service Worker Kaydı (Safari & Chrome PWA)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  });
}

// ==============================================================================
// 10. SAĞ DİKEY HEDİYE VE AÇILIM SEÇENEKLERİ GEÇİŞİ (BAN-RİSKSİZ GİFT VİDGETI)
// ==============================================================================
let giftTransitionTimer = null;
let currentGiftIndex = 0;
let isGiftLockedToReading = false;
let giftVisibilityTimeout = null;

function runGiftVisibilityLoop() {
  const showcase = document.getElementById('verticalGiftShowcase');
  if (!showcase) return;

  if (giftVisibilityTimeout) {
    clearTimeout(giftVisibilityTimeout);
    giftVisibilityTimeout = null;
  }

  // Başlangıçta görünür başlar
  showcase.classList.remove('is-hidden');

  function scheduleCycle() {
    // 10 saniye boyunca ekranda kalır
    giftVisibilityTimeout = setTimeout(() => {
      // Fal bakılıyorsa veya kullanıcıya özel açılım yapılıyorsa ekranda kalsın
      if (isGiftLockedToReading) {
        scheduleCycle();
        return;
      }

      // 10 saniye doldu: 5 saniyeliğine ekrandan kaybolsun
      showcase.classList.add('is-hidden');

      giftVisibilityTimeout = setTimeout(() => {
        // 5 saniye sonra tekrar ekranda belirsin
        showcase.classList.remove('is-hidden');
        scheduleCycle();
      }, 5000); // 5 saniye gizli kalır
    }, 10000); // 10 saniye görünür kalır
  }

  scheduleCycle();
}

function startGiftShowcaseCycle() {
  const rows = document.querySelectorAll('.gift-tier-row');
  if (!rows || rows.length === 0) return;

  if (giftTransitionTimer) {
    clearInterval(giftTransitionTimer);
    giftTransitionTimer = null;
  }

  isGiftLockedToReading = false;

  // 30 saniyede bir kaybolup 5 saniye sonra beliren döngüyü başlat
  runGiftVisibilityLoop();

  // 3.2 saniyede bir sıradaki hediyeye yumuşak ve ışıltılı canlı geçiş
  giftTransitionTimer = setInterval(() => {
    if (isGiftLockedToReading) return;
    const currentRows = document.querySelectorAll('.gift-tier-row');
    if (!currentRows || currentRows.length === 0) return;
    
    currentRows.forEach(r => r.classList.remove('active'));
    currentGiftIndex = (currentGiftIndex + 1) % currentRows.length;
    currentRows[currentGiftIndex].classList.add('active');
  }, 3200);
}

function highlightGiftTier(tierOrBadgeName) {
  const rows = document.querySelectorAll('.gift-tier-row');
  if (!rows || rows.length === 0) return;

  if (!tierOrBadgeName) {
    isGiftLockedToReading = false;
    return;
  }

  const nameLower = String(tierOrBadgeName).toLowerCase();
  let targetIdx = -1;

  if (nameLower.includes('tek kart') || nameLower.includes('beni_sev') || nameLower.includes('enerji')) {
    targetIdx = 0;
  } else if (nameLower.includes('3 kart') || nameLower.includes('donat') || nameLower.includes('kapsamlı')) {
    targetIdx = 1;
  } else if (nameLower.includes('tavsiye') || nameLower.includes('cay') || nameLower.includes('çay') || nameLower.includes('aşk bakım')) {
    targetIdx = 2;
  } else if (nameLower.includes('karışık') || nameLower.includes('karisik') || nameLower.includes('karma')) {
    targetIdx = 3;
  } else if (nameLower.includes('derin') || nameLower.includes('derin_ask')) {
    targetIdx = 4;
  } else if (nameLower.includes('kader') || nameLower.includes('dönüm')) {
    targetIdx = 5;
  }

  if (targetIdx >= 0 && rows[targetIdx]) {
    const showcase = document.getElementById('verticalGiftShowcase');
    if (showcase) showcase.classList.remove('is-hidden'); // Okuma esnasında anında göster
    isGiftLockedToReading = true;
    rows.forEach(r => r.classList.remove('active'));
    rows[targetIdx].classList.add('active');
    currentGiftIndex = targetIdx;
  }
}
