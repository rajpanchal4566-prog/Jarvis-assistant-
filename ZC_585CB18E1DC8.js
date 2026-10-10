/**
 * Split Buddy - Standalone Core Engine
 * File: ZC_585CB18E1DC8.js
 * No dependencies, runs directly in browser (file:// or http://).
 */

(function () {
  'use strict';

  // Currency Definitions with standard exchange rates relative to USD
  const CURRENCIES = [
    { code: 'USD', symbol: '$', name: 'US Dollar', rateToUSD: 1.0 },
    { code: 'EUR', symbol: '€', name: 'Euro', rateToUSD: 0.92 },
    { code: 'GBP', symbol: '£', name: 'British Pound', rateToUSD: 0.79 },
    { code: 'INR', symbol: '₹', name: 'Indian Rupee', rateToUSD: 86.5 },
    { code: 'JPY', symbol: '¥', name: 'Japanese Yen', rateToUSD: 153.2 },
    { code: 'CAD', symbol: 'C$', name: 'Canadian Dollar', rateToUSD: 1.38 },
    { code: 'AUD', symbol: 'A$', name: 'Australian Dollar', rateToUSD: 1.54 },
    { code: 'SGD', symbol: 'S$', name: 'Singapore Dollar', rateToUSD: 1.35 },
    { code: 'AED', symbol: 'AED', name: 'UAE Dirham', rateToUSD: 3.67 },
    { code: 'CHF', symbol: 'CHF', name: 'Swiss Franc', rateToUSD: 0.89 },
    { code: 'CNY', symbol: '¥', name: 'Chinese Yuan', rateToUSD: 7.24 },
    { code: 'THB', symbol: '฿', name: 'Thai Baht', rateToUSD: 36.8 }
  ];

  // Occasion Detection Rules
  const OCCASION_CATEGORIES = [
    {
      id: 'dining',
      name: 'Dining & Food',
      icon: '🍽️',
      keywords: ['dinner', 'lunch', 'brunch', 'breakfast', 'restaurant', 'food', 'meal', 'bistro', 'pizza', 'burger', 'sushi', 'taco', 'steak', 'buffet', 'eating', 'kitchen', 'pasta', 'bbq', 'takeout', 'diner']
    },
    {
      id: 'coffee',
      name: 'Coffee & Cafe',
      icon: '☕',
      keywords: ['coffee', 'cafe', 'starbucks', 'latte', 'espresso', 'cappuccino', 'bakery', 'tea', 'pastry', 'donut', 'bagel', 'boba']
    },
    {
      id: 'drinks',
      name: 'Drinks & Bar',
      icon: '🍸',
      keywords: ['bar', 'drinks', 'pub', 'beer', 'wine', 'cocktail', 'club', 'nightout', 'brewery', 'happy hour', 'beers', 'liquor', 'cocktails', 'tequila', 'whiskey']
    },
    {
      id: 'groceries',
      name: 'Groceries & Mart',
      icon: '🛒',
      keywords: ['groceries', 'grocery', 'supermarket', 'market', 'walmart', 'costco', 'trader joe', 'vegetables', 'fruits', 'milk', 'snacks', 'target', 'whole foods']
    },
    {
      id: 'travel',
      name: 'Travel & Vacation',
      icon: '✈️',
      keywords: ['trip', 'travel', 'flight', 'vacation', 'hotel', 'airbnb', 'resort', 'tour', 'holiday', 'staycation', 'lodging', 'booking', 'tokyo', 'paris', 'hostel']
    },
    {
      id: 'transport',
      name: 'Transport & Cab',
      icon: '🚗',
      keywords: ['uber', 'lyft', 'taxi', 'cab', 'gas', 'fuel', 'petrol', 'parking', 'toll', 'train', 'metro', 'bus', 'ride', 'commute']
    },
    {
      id: 'entertainment',
      name: 'Movies & Events',
      icon: '🎟️',
      keywords: ['movie', 'cinema', 'theatre', 'theater', 'concert', 'show', 'gig', 'ticket', 'bowling', 'museum', 'game', 'festival', 'amusement']
    },
    {
      id: 'housing',
      name: 'Housing & Utilities',
      icon: '🏠',
      keywords: ['rent', 'utility', 'utilities', 'electric', 'electricity', 'water', 'wifi', 'internet', 'power', 'gas bill', 'apartment', 'maintenance', 'condo']
    },
    {
      id: 'celebration',
      name: 'Party & Celebration',
      icon: '🎉',
      keywords: ['birthday', 'anniversary', 'wedding', 'party', 'celebration', 'gift', 'gifts', 'bachelor', 'bachelorette', 'farewell']
    },
    {
      id: 'fitness',
      name: 'Sports & Fitness',
      icon: '⚽',
      keywords: ['gym', 'fitness', 'workout', 'sports', 'turf', 'badminton', 'tennis', 'yoga', 'match', 'court', 'tournament']
    }
  ];

  const DEFAULT_CATEGORY = {
    id: 'general',
    name: 'General Bill',
    icon: '🧾'
  };

  // State
  let state = {
    occasion: 'Dinner with friends',
    payer: 'You',
    amount: '120.00',
    peopleCount: 4,
    tipPercent: 0,
    taxPercent: 0,
    currencyCode: 'USD',
    detectedCategory: OCCASION_CATEGORIES[0],
    currentTab: 'calculator', // 'calculator' | 'history'
    activeResult: null,
    history: [],
    customNames: [],
    paidAmounts: [], // user-entered paid amounts per person
    paymentQrImage: null, // real uploaded QR data URL
    uploadedBillImage: null // real uploaded bill receipt image
  };

  // LocalStorage Keys
  const LS_CURRENCY = 'splitbuddy_currency';
  const LS_ACTIVE = 'splitbuddy_active_bill';
  const LS_HISTORY = 'splitbuddy_history';
  const LS_PAYMENT_QR = 'splitbuddy_payment_qr';

  // DOM Elements cache
  const el = {};

  function initDOM() {
    el.occasionInput = document.getElementById('occasion-input');
    el.payerInput = document.getElementById('payer-input');
    el.amountInput = document.getElementById('amount-input');
    el.peopleInput = document.getElementById('people-input');
    el.currencySelect = document.getElementById('currency-select');
    el.currencySymbolSpan = document.getElementById('currency-symbol-span');

    el.detectedIconEl = document.getElementById('detected-icon-badge');
    el.detectedNameEl = document.getElementById('detected-category-name');

    // Bill upload
    el.btnUploadBill = document.getElementById('btn-upload-bill');
    el.billFileInput = document.getElementById('bill-file-input');
    el.uploadedBillPreviewBar = document.getElementById('uploaded-bill-preview-bar');
    el.uploadedBillImgThumb = document.getElementById('uploaded-bill-img-thumb');
    el.btnRemoveBillImg = document.getElementById('btn-remove-bill-img');
    el.billScanBanner = document.getElementById('bill-scan-banner');
    el.billScanMessage = document.getElementById('bill-scan-message');

    // Participant names
    el.btnToggleNames = document.getElementById('btn-toggle-names');
    el.optionalNamesContainer = document.getElementById('optional-names-container');
    el.namesToggleIcon = document.getElementById('names-toggle-icon');

    // Payment QR
    el.btnAttachQr = document.getElementById('btn-attach-qr');
    el.qrFileInput = document.getElementById('qr-file-input');
    el.qrPreviewBox = document.getElementById('qr-preview-box');
    el.qrPreviewImg = document.getElementById('qr-preview-img');
    el.btnRemoveQr = document.getElementById('btn-remove-qr');
    el.qrDescPlaceholder = document.getElementById('qr-desc-placeholder');

    // Result QR preview
    el.resultQrContainer = document.getElementById('result-qr-container');
    el.resultQrImg = document.getElementById('result-qr-img');
    el.resultQrPayerName = document.getElementById('result-qr-payer-name');

    el.taxButtons = document.querySelectorAll('.tax-option-btn');
    el.tipButtons = document.querySelectorAll('.tip-option-btn');
    el.taxLiveIndicator = document.getElementById('tax-live-indicator');
    el.tipLiveIndicator = document.getElementById('tip-live-indicator');
    el.peopleStepMinus = document.getElementById('btn-people-minus');
    el.peopleStepPlus = document.getElementById('btn-people-plus');
    el.quickCountButtons = document.querySelectorAll('.quick-count-btn');
    el.presetChips = document.querySelectorAll('.preset-chip');

    el.btnCalculate = document.getElementById('btn-calculate');
    el.validationBox = document.getElementById('validation-banner');
    el.validationMsg = document.getElementById('validation-message');

    el.resultCard = document.getElementById('result-card');
    el.emptyStateCard = document.getElementById('empty-state-card');

    el.perPersonHeroAmount = document.getElementById('hero-per-person');
    el.perPersonHeroSub = document.getElementById('hero-per-person-sub');
    el.statSubtotalAmount = document.getElementById('stat-subtotal-amount');
    el.statTaxAmount = document.getElementById('stat-tax-amount');
    el.statTipAmount = document.getElementById('stat-tip-amount');
    el.statTotalBill = document.getElementById('stat-total-bill');
    el.statTotalLabel = document.getElementById('stat-total-label');
    el.breakdownListContainer = document.getElementById('breakdown-list-container');
    el.multiCurrencyGrid = document.getElementById('multi-currency-grid');

    // Navigation & Tabs
    el.tabCalculator = document.getElementById('tab-calculator');
    el.tabHistory = document.getElementById('tab-history');
    el.sectionCalculator = document.getElementById('section-calculator');
    el.sectionHistory = document.getElementById('section-history');
    el.historyBadgeCount = document.getElementById('history-badge-count');

    // History elements
    el.historyListContainer = document.getElementById('history-list-container');
    el.historySearchInput = document.getElementById('history-search-input');
    el.historyEmptyState = document.getElementById('history-empty-state');
    el.btnClearHistory = document.getElementById('btn-clear-history');

    // Actions
    el.btnSaveHistory = document.getElementById('btn-save-history');
    el.btnShareReport = document.getElementById('btn-share-report');
    el.btnPrintReceipt = document.getElementById('btn-print-receipt');

    // Modals
    el.reportModal = document.getElementById('report-modal');
    el.btnCloseReportModal = document.getElementById('btn-close-report-modal');
    el.receiptContent = document.getElementById('receipt-content');
    el.btnModalWhatsapp = document.getElementById('btn-modal-whatsapp');
    el.btnModalCopy = document.getElementById('btn-modal-copy');
    el.btnModalPrint = document.getElementById('btn-modal-print');
  }

  // Detect Occasion Category
  function detectCategory(text) {
    if (!text || !text.trim()) {
      return DEFAULT_CATEGORY;
    }
    const clean = text.toLowerCase().trim();
    for (const cat of OCCASION_CATEGORIES) {
      for (const kw of cat.keywords) {
        if (clean.includes(kw)) {
          return cat;
        }
      }
    }
    return DEFAULT_CATEGORY;
  }

  function getCurrency(code) {
    return CURRENCIES.find(c => c.code === code) || CURRENCIES[0];
  }

  function formatMoney(amount, currencyCode) {
    const cur = getCurrency(currencyCode);
    const num = Number(amount) || 0;
    const decimals = currencyCode === 'JPY' ? 0 : 2;
    return `${cur.symbol}${num.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    })}`;
  }

  // Load Saved Currency & Active Bill from localStorage
  function loadPersistedData() {
    try {
      const savedCurrency = localStorage.getItem(LS_CURRENCY);
      if (savedCurrency && CURRENCIES.some(c => c.code === savedCurrency)) {
        state.currencyCode = savedCurrency;
      }

      const savedQr = localStorage.getItem(LS_PAYMENT_QR);
      if (savedQr) {
        state.paymentQrImage = savedQr;
      }

      const savedHistory = localStorage.getItem(LS_HISTORY);
      if (savedHistory) {
        state.history = JSON.parse(savedHistory);
      }

      const savedActive = localStorage.getItem(LS_ACTIVE);
      if (savedActive) {
        const parsed = JSON.parse(savedActive);
        if (parsed.occasion !== undefined) state.occasion = parsed.occasion;
        if (parsed.payer !== undefined) state.payer = parsed.payer;
        if (parsed.amount !== undefined) state.amount = String(parsed.amount);
        if (parsed.peopleCount !== undefined) state.peopleCount = Number(parsed.peopleCount);
        if (parsed.tipPercent !== undefined) state.tipPercent = Number(parsed.tipPercent);
        if (parsed.taxPercent !== undefined) state.taxPercent = Number(parsed.taxPercent);
        if (parsed.customNames !== undefined) state.customNames = parsed.customNames;
        if (parsed.paidAmounts !== undefined) state.paidAmounts = parsed.paidAmounts;
        if (parsed.uploadedBillImage !== undefined) state.uploadedBillImage = parsed.uploadedBillImage;
        if (parsed.activeResult) state.activeResult = parsed.activeResult;
      }
    } catch (e) {
      console.warn('Could not read from localStorage', e);
    }
  }

  function saveActiveState() {
    try {
      localStorage.setItem(LS_ACTIVE, JSON.stringify({
        occasion: state.occasion,
        payer: state.payer,
        amount: state.amount,
        peopleCount: state.peopleCount,
        tipPercent: state.tipPercent,
        taxPercent: state.taxPercent,
        customNames: state.customNames,
        paidAmounts: state.paidAmounts,
        uploadedBillImage: state.uploadedBillImage,
        activeResult: state.activeResult
      }));
    } catch (e) {
      console.warn('Could not save active state', e);
    }
  }

  function saveCurrencyPreference(code) {
    state.currencyCode = code;
    try {
      localStorage.setItem(LS_CURRENCY, code);
    } catch (e) {
      console.warn('Could not save currency to localStorage', e);
    }
  }

  function savePaymentQr(dataUrl) {
    state.paymentQrImage = dataUrl;
    try {
      if (dataUrl) {
        localStorage.setItem(LS_PAYMENT_QR, dataUrl);
      } else {
        localStorage.removeItem(LS_PAYMENT_QR);
      }
    } catch (e) {}
    renderPaymentQrUI();
  }

  function saveHistoryToStorage() {
    try {
      localStorage.setItem(LS_HISTORY, JSON.stringify(state.history));
    } catch (e) {
      console.warn('Could not save history to localStorage', e);
    }
    updateHistoryUI();
  }

  // Input Sanitization and Validation
  function sanitizeAmountInput(val) {
    if (typeof val !== 'string') val = String(val || '');
    const cleaned = val.replace(/[^0-9.]/g, '').trim();
    const parts = cleaned.split('.');
    if (parts.length > 2) {
      return parts[0] + '.' + parts.slice(1).join('');
    }
    return cleaned;
  }

  function validateInputs() {
    const rawAmount = state.amount ? state.amount.trim() : '';
    const numAmount = parseFloat(rawAmount);
    const people = parseInt(state.peopleCount, 10);

    if (!rawAmount || isNaN(numAmount)) {
      return {
        isValid: false,
        message: 'Please enter a valid bill amount to calculate the split.'
      };
    }

    if (numAmount <= 0) {
      return {
        isValid: false,
        message: 'Bill amount must be strictly greater than 0. Negative or zero bills cannot be split.'
      };
    }

    if (isNaN(people) || people < 1) {
      return {
        isValid: false,
        message: 'Number of people must be at least 1 person.'
      };
    }

    return {
      isValid: true,
      amount: numAmount,
      people: people
    };
  }

  // Exact Calculation Engine with Paid & Remaining tracking
  function calculateSplit() {
    const validation = validateInputs();

    if (!validation.isValid) {
      state.activeResult = null;
      renderValidation(validation.message);
      renderResults();
      saveActiveState();
      return;
    }

    hideValidation();

    const baseAmount = validation.amount;
    const people = validation.people;
    const tipPercent = state.tipPercent || 0;
    const taxPercent = state.taxPercent || 0;
    const tipAmount = Math.round((baseAmount * (tipPercent / 100)) * 100) / 100;
    const taxAmount = Math.round((baseAmount * (taxPercent / 100)) * 100) / 100;
    const totalAmount = Math.round((baseAmount + tipAmount + taxAmount) * 100) / 100;

    // Exact cent distribution math
    const totalCents = Math.round(totalAmount * 100);
    const baseShareCents = Math.floor(totalCents / people);
    const remainderCents = totalCents % people;

    const payerName = (state.payer && state.payer.trim()) || 'You';

    let totalCollected = 0;
    let totalRemaining = 0;

    const participants = [];
    for (let i = 0; i < people; i++) {
      const shareCents = baseShareCents + (i < remainderCents ? 1 : 0);
      const shareAmount = shareCents / 100;
      const isPayer = i === 0;

      let name = (state.customNames && state.customNames[i] && state.customNames[i].trim()) ||
                 (isPayer ? `${payerName} (Payer)` : `Person ${i + 1}`);

      const userPaid = (state.paidAmounts && typeof state.paidAmounts[i] === 'number') ? state.paidAmounts[i] : 0;
      const hasPaid = userPaid > 0;

      let remaining = 0;
      let isSettled = false;
      let statusText = '';

      if (hasPaid) {
        remaining = Math.max(0, Math.round((shareAmount - userPaid) * 100) / 100);
        isSettled = userPaid >= shareAmount;
        if (isSettled) {
          statusText = `Settled ✓ (Paid ${formatMoney(userPaid, state.currencyCode)})`;
        } else {
          statusText = `Paid ${formatMoney(userPaid, state.currencyCode)} · Remaining: ${formatMoney(remaining, state.currencyCode)}`;
        }
        totalCollected += Math.min(userPaid, shareAmount);
        totalRemaining += remaining;
      } else {
        // If user doesn't add it, give it as it is!
        if (isPayer) {
          remaining = 0;
          isSettled = true;
          statusText = `Paid total bill ${formatMoney(totalAmount, state.currencyCode)}`;
          totalCollected += shareAmount;
        } else {
          remaining = shareAmount;
          isSettled = false;
          statusText = `Owes ${formatMoney(shareAmount, state.currencyCode)} to ${payerName}`;
          totalRemaining += remaining;
        }
      }

      participants.push({
        index: i + 1,
        name: name,
        isPayer: isPayer,
        share: shareAmount,
        paidAmount: userPaid,
        remainingAmount: remaining,
        isSettled: isSettled,
        status: statusText
      });
    }

    const averagePerPerson = totalAmount / people;

    state.activeResult = {
      occasion: state.occasion.trim() || 'General Expense',
      category: state.detectedCategory,
      currencyCode: state.currencyCode,
      baseAmount: baseAmount,
      tipPercent: tipPercent,
      tipAmount: tipAmount,
      taxPercent: taxPercent,
      taxAmount: taxAmount,
      totalAmount: totalAmount,
      peopleCount: people,
      perPersonAverage: averagePerPerson,
      participants: participants,
      totalCollected: Math.round(totalCollected * 100) / 100,
      totalRemaining: Math.round(totalRemaining * 100) / 100,
      calculatedAt: new Date().toISOString(),
      paymentQrImage: state.paymentQrImage,
      uploadedBillImage: state.uploadedBillImage
    };

    renderResults();
    saveActiveState();
  }

  // Parse Receipt Text/Filename Heuristics
  function parseReceiptDetails(text, filename) {
    let detectedAmount = null;
    let detectedPeople = null;
    let detectedOccasion = null;
    const notes = [];

    const fullStr = (text || '') + '\n' + (filename || '');

    const peopleMatches = fullStr.match(/(?:guests?|covers?|party\s+of|split|people|persons?|pax)\s*[:#=\-]?\s*(\d{1,2})\b/i);
    if (peopleMatches && peopleMatches[1]) {
      const p = parseInt(peopleMatches[1], 10);
      if (p >= 1 && p <= 50) {
        detectedPeople = p;
        notes.push(`Detected ${p} guests / people`);
      }
    }

    const totalMatches = fullStr.match(/(?:grand\s+total|total\s+due|total\s+amount|net\s+total|total|amount|balance)\s*[:#=\-]?\s*[$€£₹¥]?\s*(\d+(?:[.,]\d{2}))/i);
    if (totalMatches && totalMatches[1]) {
      const num = parseFloat(totalMatches[1].replace(',', '.'));
      if (!isNaN(num) && num > 0) {
        detectedAmount = num;
        notes.push(`Detected total: ${num.toFixed(2)}`);
      }
    } else {
      const allCur = fullStr.match(/[$€£₹¥]\s*(\d+(?:[.,]\d{2}))/g);
      if (allCur && allCur.length > 0) {
        const nums = allCur.map(a => {
          const m = a.match(/(\d+(?:[.,]\d{2}))/);
          return m ? parseFloat(m[1].replace(',', '.')) : 0;
        });
        const mx = Math.max(...nums);
        if (mx > 0) {
          detectedAmount = mx;
          notes.push(`Detected probable total: ${mx.toFixed(2)}`);
        }
      }
    }

    const vendorMap = {
      bistro: 'Dinner at Bistro',
      restaurant: 'Restaurant Dining',
      cafe: 'Cafe & Coffee',
      starbucks: 'Starbucks Coffee',
      uber: 'Uber Ride',
      lyft: 'Lyft Ride',
      taxi: 'Taxi Fare',
      walmart: 'Walmart Groceries',
      costco: 'Costco Supplies',
      target: 'Target Shopping',
      groceries: 'Grocery Run',
      hotel: 'Hotel & Lodging',
      pizza: 'Pizza Night',
      burger: 'Burgers & Fries'
    };

    const lower = fullStr.toLowerCase();
    for (const [kw, occ] of Object.entries(vendorMap)) {
      if (lower.includes(kw)) {
        detectedOccasion = occ;
        notes.push(`Identified occasion: ${occ}`);
        break;
      }
    }

    if (!detectedOccasion && filename) {
      const cleanName = filename.replace(/\.[^/.]+$/, '').replace(/[_\-+]/g, ' ').trim();
      if (cleanName.length > 2 && !cleanName.match(/^image\d*$/i) && !cleanName.match(/^receipt\d*$/i)) {
        detectedOccasion = cleanName.charAt(0).toUpperCase() + cleanName.slice(1);
      }
    }

    return { detectedAmount, detectedPeople, detectedOccasion, notes };
  }

  // Render Functions
  function renderValidation(msg) {
    if (el.validationBox && el.validationMsg) {
      el.validationMsg.textContent = msg;
      el.validationBox.style.display = 'flex';
    }
  }

  function hideValidation() {
    if (el.validationBox) {
      el.validationBox.style.display = 'none';
    }
  }

  function renderCategory() {
    const cat = detectCategory(state.occasion);
    state.detectedCategory = cat;
    if (el.detectedIconEl) el.detectedIconEl.textContent = cat.icon;
    if (el.detectedNameEl) el.detectedNameEl.textContent = cat.name;
  }

  function renderCurrency() {
    const cur = getCurrency(state.currencyCode);
    if (el.currencySelect) el.currencySelect.value = state.currencyCode;
    if (el.currencySymbolSpan) el.currencySymbolSpan.textContent = cur.symbol;

    if (state.activeResult) {
      state.activeResult.currencyCode = state.currencyCode;
      renderResults();
    }
  }

  function renderPaymentQrUI() {
    if (state.paymentQrImage) {
      if (el.qrPreviewBox) el.qrPreviewBox.style.display = 'flex';
      if (el.qrPreviewImg) el.qrPreviewImg.src = state.paymentQrImage;
      if (el.qrDescPlaceholder) el.qrDescPlaceholder.style.display = 'none';
      if (el.btnAttachQr) el.btnAttachQr.style.display = 'none';
    } else {
      if (el.qrPreviewBox) el.qrPreviewBox.style.display = 'none';
      if (el.qrDescPlaceholder) el.qrDescPlaceholder.style.display = 'block';
      if (el.btnAttachQr) el.btnAttachQr.style.display = 'inline-flex';
    }
  }

  function renderUploadedBillUI() {
    if (state.uploadedBillImage) {
      if (el.uploadedBillPreviewBar) el.uploadedBillPreviewBar.style.display = 'flex';
      if (el.uploadedBillImgThumb) el.uploadedBillImgThumb.src = state.uploadedBillImage;
    } else {
      if (el.uploadedBillPreviewBar) el.uploadedBillPreviewBar.style.display = 'none';
    }
  }

  function renderParticipantNamesInputGrid() {
    if (!el.optionalNamesContainer) return;
    el.optionalNamesContainer.innerHTML = '';

    const count = state.peopleCount || 1;
    const payerName = (state.payer && state.payer.trim()) || 'You';

    for (let i = 0; i < count; i++) {
      const isPayer = i === 0;
      const placeholder = isPayer ? `${payerName} (Payer)` : `Person ${i + 1}`;
      const currentVal = state.customNames[i] || '';

      const wrap = document.createElement('div');
      wrap.style.display = 'flex';
      wrap.style.alignItems = 'center';
      wrap.style.gap = '0.5rem';

      wrap.innerHTML = `
        <span style="font-size: 0.8125rem; font-weight: 700; color: #64748b; width: 24px;">#${i + 1}</span>
        <input
          type="text"
          class="form-input participant-name-input"
          data-index="${i}"
          placeholder="${escapeHTML(placeholder)}"
          value="${escapeHTML(currentVal)}"
          style="padding: 0.4rem 0.65rem; font-size: 0.875rem;"
        />
      `;

      el.optionalNamesContainer.appendChild(wrap);
    }

    el.optionalNamesContainer.querySelectorAll('.participant-name-input').forEach(input => {
      input.addEventListener('input', (e) => {
        const idx = parseInt(e.target.getAttribute('data-index'), 10);
        state.customNames[idx] = e.target.value;
        saveActiveState();
        calculateSplit();
      });
    });
  }

  function renderResults() {
    const res = state.activeResult;

    if (!res) {
      if (el.resultCard) el.resultCard.style.display = 'none';
      if (el.emptyStateCard) el.emptyStateCard.style.display = 'block';
      return;
    }

    if (el.emptyStateCard) el.emptyStateCard.style.display = 'none';
    if (el.resultCard) el.resultCard.style.display = 'block';

    const cur = state.currencyCode;
    const hasAnyCustomPaid = res.participants.some(p => p.paidAmount > 0);

    // Hero stat
    if (el.perPersonHeroAmount) {
      el.perPersonHeroAmount.textContent = formatMoney(res.perPersonAverage, cur);
    }
    if (el.perPersonHeroSub) {
      el.perPersonHeroSub.textContent = `Exact per-person share across ${res.peopleCount} ${res.peopleCount === 1 ? 'person' : 'people'}`;
    }

    // Mini stats: Subtotal, Tax, Tip, Total / Remaining
    if (el.statSubtotalAmount) el.statSubtotalAmount.textContent = formatMoney(res.baseAmount, cur);
    if (el.statTaxAmount) {
      el.statTaxAmount.textContent = res.taxAmount > 0
        ? `${formatMoney(res.taxAmount, cur)} (${res.taxPercent}%)`
        : '0.00 (0%)';
    }
    if (el.statTipAmount) {
      el.statTipAmount.textContent = res.tipAmount > 0
        ? `${formatMoney(res.tipAmount, cur)} (${res.tipPercent}%)`
        : '0.00 (0%)';
    }
    if (el.statTotalBill) {
      if (hasAnyCustomPaid && res.totalRemaining !== undefined) {
        el.statTotalBill.textContent = formatMoney(res.totalRemaining, cur);
        el.statTotalBill.style.color = '#b45309';
        if (el.statTotalLabel) el.statTotalLabel.textContent = 'Remaining Unpaid';
      } else {
        el.statTotalBill.textContent = formatMoney(res.totalAmount, cur);
        el.statTotalBill.style.color = '#065f46';
        if (el.statTotalLabel) el.statTotalLabel.textContent = 'Total Bill';
      }
    }

    // Live Indicators
    if (el.taxLiveIndicator) {
      el.taxLiveIndicator.textContent = res.taxPercent > 0
        ? `+${res.taxPercent}% (${formatMoney(res.taxAmount, cur)})`
        : '0% (No Tax)';
    }
    if (el.tipLiveIndicator) {
      el.tipLiveIndicator.textContent = res.tipPercent > 0
        ? `+${res.tipPercent}% (${formatMoney(res.tipAmount, cur)})`
        : '0% (No Tip)';
    }

    // Render Participant Breakdown List with Paid & Remaining tracking
    if (el.breakdownListContainer) {
      el.breakdownListContainer.innerHTML = '';
      res.participants.forEach((p, idx) => {
        const row = document.createElement('div');
        row.className = 'person-item-row';
        row.style.flexDirection = 'column';
        row.style.alignItems = 'stretch';
        row.style.gap = '0.5rem';

        const isPayer = p.isPayer;
        const initials = isPayer ? '⭐' : `P${p.index}`;
        const hasPaid = p.paidAmount > 0;

        row.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div class="person-info">
              <div class="person-avatar ${isPayer ? 'payer' : ''}">${initials}</div>
              <div>
                <div class="person-name">${escapeHTML(p.name)}</div>
                <div class="person-status">${escapeHTML(p.status)}</div>
              </div>
            </div>
            <div class="person-amount-box">
              <div class="person-exact-amount tabular-nums">${formatMoney(p.share, cur)}</div>
              <div class="person-exact-status ${isPayer ? 'status-paid' : 'status-owes'}">
                ${isPayer ? 'Net Receives ' + formatMoney(res.totalAmount - p.share, cur) : 'Share'}
              </div>
            </div>
          </div>

          <!-- Paid and Remaining Control Row (Optional) -->
          <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 0.5rem; border-top: 1px dashed #e2e8f0; font-size: 0.8125rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #64748b;">Paid so far:</span>
              <div style="position: relative; display: flex; align-items: center; width: 90px;">
                <span style="position: absolute; left: 6px; font-size: 0.75rem; color: #94a3b8; font-family: monospace;">${getCurrency(cur).symbol}</span>
                <input
                  type="number"
                  step="any"
                  min="0"
                  placeholder="0.00"
                  class="form-input row-paid-input"
                  data-idx="${idx}"
                  value="${hasPaid ? p.paidAmount : ''}"
                  style="padding: 0.25rem 0.4rem 0.25rem 1.25rem; font-size: 0.8125rem; font-weight: 700; font-family: monospace;"
                />
              </div>
              <button
                type="button"
                class="btn-quick-full-pay"
                data-idx="${idx}"
                style="padding: 0.25rem 0.5rem; font-size: 0.6875rem; font-weight: 700; background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; border-radius: 4px; cursor: pointer;"
              >
                Paid Full
              </button>
              ${hasPaid ? `
                <button
                  type="button"
                  class="btn-reset-paid"
                  data-idx="${idx}"
                  style="background: transparent; border: none; color: #94a3b8; cursor: pointer; padding: 2px;"
                  title="Reset to 0 (as it is)"
                >
                  ✕
                </button>
              ` : ''}
            </div>

            <div>
              ${hasPaid ? (
                p.isSettled ? `
                  <span style="font-size: 0.75rem; font-weight: 700; color: #059669; background: #ecfdf5; padding: 2px 8px; border-radius: 9999px;">
                    Settled ✓ (0 Rem)
                  </span>
                ` : `
                  <span style="font-size: 0.75rem; font-weight: 700; color: #b45309; background: #fef3c7; padding: 2px 8px; border-radius: 9999px;" class="tabular-nums">
                    Rem: ${formatMoney(p.remainingAmount, cur)}
                  </span>
                `
              ) : `
                <span style="font-size: 0.75rem; color: #64748b;">
                  ${isPayer ? 'Paid total' : 'Remaining: ' + formatMoney(p.share, cur)}
                </span>
              `}
            </div>
          </div>
        `;
        el.breakdownListContainer.appendChild(row);
      });

      // Attach row input listeners
      el.breakdownListContainer.querySelectorAll('.row-paid-input').forEach(inp => {
        inp.addEventListener('input', (e) => {
          const idx = parseInt(e.target.getAttribute('data-idx'), 10);
          const val = parseFloat(e.target.value);
          state.paidAmounts[idx] = isNaN(val) ? 0 : Math.max(0, val);
          calculateSplit();
        });
      });

      el.breakdownListContainer.querySelectorAll('.btn-quick-full-pay').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const idx = parseInt(e.target.getAttribute('data-idx'), 10);
          if (res.participants[idx]) {
            state.paidAmounts[idx] = res.participants[idx].share;
            calculateSplit();
          }
        });
      });

      el.breakdownListContainer.querySelectorAll('.btn-reset-paid').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const idx = parseInt(e.target.getAttribute('data-idx'), 10);
          state.paidAmounts[idx] = 0;
          calculateSplit();
        });
      });
    }

    // Render QR code on result card if attached
    if (state.paymentQrImage && el.resultQrContainer && el.resultQrImg) {
      el.resultQrContainer.style.display = 'flex';
      el.resultQrImg.src = state.paymentQrImage;
      if (el.resultQrPayerName) {
        el.resultQrPayerName.textContent = (state.payer && state.payer.trim()) || 'Payer';
      }
    } else if (el.resultQrContainer) {
      el.resultQrContainer.style.display = 'none';
    }

    // Render Multi-Currency Table
    renderMultiCurrency(res.totalAmount, res.perPersonAverage, cur);
  }

  function renderMultiCurrency(totalAmount, perPersonAmount, baseCurrencyCode) {
    if (!el.multiCurrencyGrid) return;
    el.multiCurrencyGrid.innerHTML = '';

    const baseCurrency = getCurrency(baseCurrencyCode);
    const amountInUSD = totalAmount / baseCurrency.rateToUSD;
    const perPersonInUSD = perPersonAmount / baseCurrency.rateToUSD;

    const targetCurrencies = CURRENCIES.filter(c => c.code !== baseCurrencyCode).slice(0, 6);

    targetCurrencies.forEach(target => {
      const convertedTotal = amountInUSD * target.rateToUSD;
      const convertedPerPerson = perPersonInUSD * target.rateToUSD;

      const item = document.createElement('div');
      item.className = 'currency-item-box';
      item.innerHTML = `
        <div>
          <span class="currency-code-tag">${target.code} (${target.symbol})</span>
        </div>
        <div style="text-align: right;">
          <div class="currency-converted-val tabular-nums">${formatMoney(convertedPerPerson, target.code)}<span style="font-size: 0.75rem; color: #64748b; font-weight: normal;"> / person</span></div>
          <div style="font-size: 0.75rem; color: #64748b;" class="tabular-nums">Total: ${formatMoney(convertedTotal, target.code)}</div>
        </div>
      `;
      el.multiCurrencyGrid.appendChild(item);
    });
  }

  // History System
  function saveCurrentBillToHistory() {
    if (!state.activeResult) {
      showToast('Please calculate a valid bill before saving to history.');
      return;
    }

    const newItem = {
      id: 'bill_' + Date.now(),
      occasion: state.activeResult.occasion,
      category: state.activeResult.category,
      payer: (state.payer && state.payer.trim()) || 'You',
      baseAmount: state.activeResult.baseAmount,
      totalAmount: state.activeResult.totalAmount,
      currencyCode: state.activeResult.currencyCode,
      peopleCount: state.activeResult.peopleCount,
      perPersonAverage: state.activeResult.perPersonAverage,
      tipPercent: state.activeResult.tipPercent,
      tipAmount: state.activeResult.tipAmount,
      taxPercent: state.activeResult.taxPercent,
      taxAmount: state.activeResult.taxAmount,
      date: new Date().toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      participants: state.activeResult.participants,
      totalCollected: state.activeResult.totalCollected,
      totalRemaining: state.activeResult.totalRemaining,
      paymentQrImage: state.paymentQrImage,
      uploadedBillImage: state.uploadedBillImage
    };

    state.history.unshift(newItem);
    saveHistoryToStorage();
    showToast('✓ Bill successfully saved to History!');
  }

  function updateHistoryUI() {
    if (el.historyBadgeCount) {
      el.historyBadgeCount.textContent = state.history.length;
    }

    if (!el.historyListContainer) return;
    el.historyListContainer.innerHTML = '';

    const filterText = (el.historySearchInput && el.historySearchInput.value || '').toLowerCase().trim();
    const filtered = state.history.filter(item => {
      if (!filterText) return true;
      return item.occasion.toLowerCase().includes(filterText) ||
             item.payer.toLowerCase().includes(filterText) ||
             item.currencyCode.toLowerCase().includes(filterText);
    });

    if (filtered.length === 0) {
      if (el.historyEmptyState) el.historyEmptyState.style.display = 'block';
      return;
    }

    if (el.historyEmptyState) el.historyEmptyState.style.display = 'none';

    filtered.forEach(item => {
      const card = document.createElement('div');
      card.className = 'history-item-card';

      const icon = item.category ? item.category.icon : '🧾';

      card.innerHTML = `
        <div class="history-item-top">
          <div class="history-occasion-badge">
            <div class="history-icon-circle">${icon}</div>
            <div>
              <div class="history-item-name">${escapeHTML(item.occasion)}</div>
              <div class="history-item-meta">Paid by ${escapeHTML(item.payer)} · ${item.date}</div>
            </div>
          </div>
          <button class="modal-close-btn btn-delete-history" data-id="${item.id}" title="Delete record" style="font-size: 1.15rem; color: #94a3b8;">&times;</button>
        </div>

        <div class="history-amounts-box">
          <div>
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700;">Per Person (${item.peopleCount} ppl)</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #065f46;" class="tabular-nums">${formatMoney(item.perPersonAverage, item.currencyCode)}</div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 0.75rem; text-transform: uppercase; color: #64748b; font-weight: 700;">Total Bill</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a;" class="tabular-nums">${formatMoney(item.totalAmount, item.currencyCode)}</div>
          </div>
        </div>

        <div class="history-actions">
          <button class="btn-secondary btn-load-history" data-id="${item.id}" style="padding: 0.45rem 0.75rem; font-size: 0.8125rem;">
            Load to Calculator
          </button>
          <button class="btn-secondary btn-view-report" data-id="${item.id}" style="padding: 0.45rem 0.75rem; font-size: 0.8125rem;">
            Report / Receipt
          </button>
        </div>
      `;

      el.historyListContainer.appendChild(card);
    });

    el.historyListContainer.querySelectorAll('.btn-delete-history').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        deleteHistoryItem(id);
      });
    });

    el.historyListContainer.querySelectorAll('.btn-load-history').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        loadHistoryItemToCalculator(id);
      });
    });

    el.historyListContainer.querySelectorAll('.btn-view-report').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        const item = state.history.find(h => h.id === id);
        if (item) {
          openReportModalWithItem(item);
        }
      });
    });
  }

  function deleteHistoryItem(id) {
    state.history = state.history.filter(h => h.id !== id);
    saveHistoryToStorage();
    showToast('Record deleted.');
  }

  function loadHistoryItemToCalculator(id) {
    const item = state.history.find(h => h.id === id);
    if (!item) return;

    state.occasion = item.occasion;
    state.payer = item.payer;
    state.amount = String(item.baseAmount || item.totalAmount);
    state.peopleCount = item.peopleCount;
    state.tipPercent = item.tipPercent || 0;
    state.taxPercent = item.taxPercent || 0;
    state.customNames = item.participants?.map(p => p.name) || [];
    state.paidAmounts = item.participants?.map(p => p.paidAmount) || [];
    saveCurrencyPreference(item.currencyCode);

    if (item.paymentQrImage) {
      savePaymentQr(item.paymentQrImage);
    }
    if (item.uploadedBillImage) {
      state.uploadedBillImage = item.uploadedBillImage;
      renderUploadedBillUI();
    }

    if (el.occasionInput) el.occasionInput.value = state.occasion;
    if (el.payerInput) el.payerInput.value = state.payer;
    if (el.amountInput) el.amountInput.value = state.amount;
    if (el.peopleInput) el.peopleInput.value = state.peopleCount;

    if (el.taxButtons) {
      el.taxButtons.forEach(b => {
        const val = parseInt(b.getAttribute('data-tax'), 10);
        b.classList.toggle('active', val === state.taxPercent);
      });
    }

    if (el.tipButtons) {
      el.tipButtons.forEach(b => {
        const val = parseInt(b.getAttribute('data-tip'), 10);
        b.classList.toggle('active', val === state.tipPercent);
      });
    }

    syncQuickPeopleButtons(state.peopleCount);
    switchTab('calculator');
    renderCategory();
    renderCurrency();
    renderParticipantNamesInputGrid();
    calculateSplit();
    showToast('✓ Loaded record into calculator');
  }

  // Report & Sharing
  function generateShareText(bill) {
    const cur = bill.currencyCode;
    const catIcon = bill.category ? bill.category.icon : '🧾';
    const hasAnyPaid = (bill.participants || []).some(p => p.paidAmount > 0);

    const lines = [
      `${catIcon} *Split Buddy Bill Summary: ${bill.occasion}*`,
      `━━━━━━━━━━━━━━━━━━━━━━━━━━`
    ];

    if (bill.baseAmount && (bill.taxAmount || bill.tipAmount)) {
      lines.push(`• Subtotal / Base: ${formatMoney(bill.baseAmount, cur)}`);
    }
    if (bill.taxAmount && bill.taxAmount > 0) {
      lines.push(`• Tax (${bill.taxPercent || 0}%): ${formatMoney(bill.taxAmount, cur)}`);
    }
    if (bill.tipAmount && bill.tipAmount > 0) {
      lines.push(`• Tip (${bill.tipPercent || 0}%): ${formatMoney(bill.tipAmount, cur)}`);
    }

    lines.push(`• *Total Bill: ${formatMoney(bill.totalAmount, cur)}*`);
    lines.push(`• Split Between: ${bill.peopleCount} people`);
    lines.push(`• *Each Person's Share: ${formatMoney(bill.perPersonAverage, cur)}*`);
    lines.push(`• Paid by: ${bill.payer || 'You'}`);

    if (hasAnyPaid && bill.totalRemaining !== undefined) {
      lines.push(`• *Total Remaining Unpaid: ${formatMoney(bill.totalRemaining, cur)}*`);
    }

    lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    lines.push(`*Individual Breakdown:*`);

    if (bill.participants && bill.participants.length) {
      bill.participants.forEach(p => {
        if (p.paidAmount > 0) {
          if (p.isSettled) {
            lines.push(`- ${p.name}: Share ${formatMoney(p.share, cur)} | Paid: ${formatMoney(p.paidAmount, cur)} | Settled ✓`);
          } else {
            lines.push(`- ${p.name}: Share ${formatMoney(p.share, cur)} | Paid: ${formatMoney(p.paidAmount, cur)} | *Remaining: ${formatMoney(p.remainingAmount, cur)}*`);
          }
        } else {
          // As it is
          lines.push(`- ${p.name}: ${formatMoney(p.share, cur)} (${p.isPayer ? 'Paid' : 'Owes'})`);
        }
      });
    }

    if (bill.paymentQrImage) {
      lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      lines.push(`📱 Payment QR attached on official receipt — scan to pay ${bill.payer || 'Payer'} directly.`);
    }

    lines.push(`━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    lines.push(`Generated accurately with Split Buddy.`);
    return lines.join('\n');
  }

  function openReportModalWithItem(item) {
    const bill = item || state.activeResult;
    if (!bill) {
      showToast('No active bill to report.');
      return;
    }

    const shareText = generateShareText(bill);
    const cur = bill.currencyCode;
    const icon = bill.category ? bill.category.icon : '🧾';
    const qrImg = bill.paymentQrImage || state.paymentQrImage;
    const hasAnyPaid = (bill.participants || []).some(p => p.paidAmount > 0);

    if (el.receiptContent) {
      el.receiptContent.innerHTML = `
        <div class="receipt-header">
          <div style="font-size: 2rem; margin-bottom: 0.25rem;">${icon}</div>
          <div class="receipt-brand-title">Split Buddy — Official Receipt</div>
          <div style="font-size: 0.8125rem; color: #64748b; margin-top: 0.35rem;">${bill.date || new Date().toLocaleString()}</div>
        </div>

        <div class="receipt-row">
          <span style="color: #64748b;">Occasion / Purpose</span>
          <strong>${escapeHTML(bill.occasion)}</strong>
        </div>
        <div class="receipt-row">
          <span style="color: #64748b;">Paid by</span>
          <strong>${escapeHTML(bill.payer || 'You')}</strong>
        </div>
        <div class="receipt-row">
          <span style="color: #64748b;">Total People</span>
          <strong>${bill.peopleCount}</strong>
        </div>
        ${bill.baseAmount && (bill.taxAmount || bill.tipAmount) ? `
        <div class="receipt-row">
          <span style="color: #64748b;">Subtotal / Base</span>
          <span class="tabular-nums font-bold">${formatMoney(bill.baseAmount, cur)}</span>
        </div>` : ''}
        ${bill.taxAmount ? `
        <div class="receipt-row">
          <span style="color: #64748b;">Tax / VAT (${bill.taxPercent}%)</span>
          <span class="tabular-nums font-bold">${formatMoney(bill.taxAmount, cur)}</span>
        </div>` : ''}
        ${bill.tipAmount ? `
        <div class="receipt-row">
          <span style="color: #64748b;">Tip (${bill.tipPercent}%)</span>
          <span class="tabular-nums font-bold">${formatMoney(bill.tipAmount, cur)}</span>
        </div>` : ''}

        <div class="receipt-total-row receipt-row">
          <span>Total Bill</span>
          <span class="tabular-nums" style="color: #065f46;">${formatMoney(bill.totalAmount, cur)}</span>
        </div>

        ${hasAnyPaid && bill.totalRemaining !== undefined ? `
          <div style="display: flex; justify-content: space-between; padding: 0.5rem; background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; font-weight: 700; color: #92400e; font-size: 0.875rem; margin-top: 0.5rem;">
            <span>Remaining Unpaid</span>
            <span class="tabular-nums">${formatMoney(bill.totalRemaining, cur)}</span>
          </div>
        ` : ''}

        <div style="margin: 1.25rem 0 0.5rem 0; font-size: 0.8125rem; font-weight: 700; text-transform: uppercase; color: #64748b; border-bottom: 1px dashed #cbd5e1; padding-bottom: 0.35rem;">
          Itemized Distribution ${hasAnyPaid ? '(With Payments)' : ''}
        </div>

        ${(bill.participants || []).map(p => `
          <div class="receipt-row" style="font-size: 0.875rem; align-items: center;">
            <div>
              <span>${escapeHTML(p.name)}</span>
              ${p.paidAmount > 0 ? `<span style="font-size: 0.75rem; color: #64748b; display: block;">Paid: ${formatMoney(p.paidAmount, cur)}</span>` : ''}
            </div>
            <div style="text-align: right;">
              <span class="tabular-nums" style="font-weight: 700; display: block;">${formatMoney(p.share, cur)}</span>
              ${p.paidAmount > 0 ? (
                p.isSettled
                  ? `<span style="font-size: 0.75rem; color: #059669; font-weight: 700;">Settled ✓</span>`
                  : `<span style="font-size: 0.75rem; color: #b45309; font-weight: 700;" class="tabular-nums">Rem: ${formatMoney(p.remainingAmount, cur)}</span>`
              ) : ''}
            </div>
          </div>
        `).join('')}

        ${qrImg ? `
          <div style="text-align: center; margin-top: 1.25rem; padding-top: 1rem; border-top: 1px dashed #cbd5e1;">
            <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #475569; display: block; margin-bottom: 0.5rem;">
              Scan QR to Pay ${escapeHTML(bill.payer || 'Payer')}
            </span>
            <div style="display: inline-block; padding: 6px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px;">
              <img src="${qrImg}" alt="Payment QR" style="width: 140px; height: 140px; object-fit: contain; display: block;" />
            </div>
            <span style="font-size: 0.75rem; color: #64748b; display: block; margin-top: 0.35rem;">
              Open camera, UPI, PayPal, or Venmo app to pay
            </span>
          </div>
        ` : ''}

        <div style="text-align: center; margin-top: 1.25rem; font-size: 0.75rem; color: #94a3b8;">
          All shares exact to the penny. Thank you for splitting cleanly!
        </div>
      `;
    }

    if (el.btnModalWhatsapp) {
      el.btnModalWhatsapp.onclick = () => {
        const url = `https://wa.me/?text=${encodeURIComponent(shareText)}`;
        window.open(url, '_blank');
      };
    }

    if (el.btnModalCopy) {
      el.btnModalCopy.onclick = () => {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(shareText).then(() => {
            showToast('✓ Bill report copied to clipboard!');
          }).catch(() => {
            fallbackCopyText(shareText);
          });
        } else {
          fallbackCopyText(shareText);
        }
      };
    }

    if (el.btnModalPrint) {
      el.btnModalPrint.onclick = () => {
        window.print();
      };
    }

    if (el.reportModal) {
      el.reportModal.style.display = 'flex';
    }
  }

  function fallbackCopyText(text) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {
      document.execCommand('copy');
      showToast('✓ Bill report copied to clipboard!');
    } catch (err) {
      showToast('Failed to copy.');
    }
    document.body.removeChild(ta);
  }

  function showToast(msg) {
    const old = document.querySelector('.toast-notice');
    if (old) old.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-notice';
    toast.textContent = msg;
    document.body.appendChild(toast);

    setTimeout(() => {
      if (toast && toast.parentNode) {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
      }
    }, 3000);
  }

  function switchTab(tabId) {
    state.currentTab = tabId;

    if (el.tabCalculator) {
      el.tabCalculator.classList.toggle('active', tabId === 'calculator');
    }
    if (el.tabHistory) {
      el.tabHistory.classList.toggle('active', tabId === 'history');
    }

    if (el.sectionCalculator) {
      if (tabId === 'calculator') {
        el.sectionCalculator.classList.remove('hidden');
      } else {
        el.sectionCalculator.classList.add('hidden');
      }
    }

    if (el.sectionHistory) {
      if (tabId === 'history') {
        el.sectionHistory.classList.add('active');
        updateHistoryUI();
      } else {
        el.sectionHistory.classList.remove('active');
      }
    }
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  }

  // Bind Event Handlers
  function bindEvents() {
    if (el.occasionInput) {
      el.occasionInput.addEventListener('input', (e) => {
        state.occasion = e.target.value;
        renderCategory();
        saveActiveState();
      });
    }

    if (el.payerInput) {
      el.payerInput.addEventListener('input', (e) => {
        state.payer = e.target.value;
        saveActiveState();
        renderParticipantNamesInputGrid();
      });
    }

    if (el.amountInput) {
      el.amountInput.addEventListener('input', (e) => {
        const sanitized = sanitizeAmountInput(e.target.value);
        state.amount = sanitized;
        if (e.target.value !== sanitized && !e.target.value.endsWith('.')) {
          e.target.value = sanitized;
        }
        saveActiveState();
      });

      el.amountInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          calculateSplit();
        }
      });
    }

    if (el.peopleInput) {
      el.peopleInput.addEventListener('input', (e) => {
        let val = parseInt(e.target.value.replace(/[^0-9]/g, ''), 10);
        if (isNaN(val) || val < 1) val = 1;
        state.peopleCount = val;
        syncQuickPeopleButtons(val);
        renderParticipantNamesInputGrid();
        saveActiveState();
      });
    }

    if (el.peopleStepMinus) {
      el.peopleStepMinus.addEventListener('click', () => {
        if (state.peopleCount > 1) {
          state.peopleCount--;
          if (el.peopleInput) el.peopleInput.value = state.peopleCount;
          syncQuickPeopleButtons(state.peopleCount);
          renderParticipantNamesInputGrid();
          saveActiveState();
          calculateSplit();
        }
      });
    }

    if (el.peopleStepPlus) {
      el.peopleStepPlus.addEventListener('click', () => {
        state.peopleCount++;
        if (el.peopleInput) el.peopleInput.value = state.peopleCount;
        syncQuickPeopleButtons(state.peopleCount);
        renderParticipantNamesInputGrid();
        saveActiveState();
        calculateSplit();
      });
    }

    el.quickCountButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const count = parseInt(e.target.getAttribute('data-count'), 10);
        state.peopleCount = count;
        if (el.peopleInput) el.peopleInput.value = count;
        syncQuickPeopleButtons(count);
        renderParticipantNamesInputGrid();
        saveActiveState();
        calculateSplit();
      });
    });

    el.presetChips.forEach(chip => {
      chip.addEventListener('click', (e) => {
        const title = e.target.getAttribute('data-name');
        if (title) {
          state.occasion = title;
          if (el.occasionInput) el.occasionInput.value = title;
          renderCategory();
          saveActiveState();
        }
      });
    });

    if (el.btnToggleNames && el.optionalNamesContainer) {
      el.btnToggleNames.addEventListener('click', () => {
        const isOpen = el.optionalNamesContainer.style.display !== 'none';
        el.optionalNamesContainer.style.display = isOpen ? 'none' : 'grid';
        if (el.namesToggleIcon) {
          el.namesToggleIcon.textContent = isOpen ? '▾' : '▴';
        }
        if (!isOpen) {
          renderParticipantNamesInputGrid();
        }
      });
    }

    if (el.btnUploadBill && el.billFileInput) {
      el.btnUploadBill.addEventListener('click', () => {
        el.billFileInput.click();
      });

      el.billFileInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        const reader = new FileReader();

        if (file.type.startsWith('image/')) {
          reader.onload = (ev) => {
            state.uploadedBillImage = ev.target.result;
            renderUploadedBillUI();
            const parsed = parseReceiptDetails('', file.name);
            handleParsedBill(parsed, file.name);
          };
          reader.readAsDataURL(file);
        } else {
          reader.onload = (ev) => {
            const text = ev.target.result || '';
            const parsed = parseReceiptDetails(text, file.name);
            handleParsedBill(parsed, file.name);
          };
          reader.readAsText(file);
        }
      });
    }

    if (el.btnRemoveBillImg) {
      el.btnRemoveBillImg.addEventListener('click', () => {
        state.uploadedBillImage = null;
        renderUploadedBillUI();
        if (el.billFileInput) el.billFileInput.value = '';
        saveActiveState();
      });
    }

    function handleParsedBill(parsed, filename) {
      const msgs = [];
      if (parsed.detectedAmount && parsed.detectedAmount > 0) {
        state.amount = parsed.detectedAmount.toFixed(2);
        if (el.amountInput) el.amountInput.value = state.amount;
        msgs.push(`Amount: ${state.amount}`);
      }
      if (parsed.detectedPeople && parsed.detectedPeople >= 1) {
        state.peopleCount = parsed.detectedPeople;
        if (el.peopleInput) el.peopleInput.value = state.peopleCount;
        syncQuickPeopleButtons(state.peopleCount);
        renderParticipantNamesInputGrid();
        msgs.push(`Split: ${state.peopleCount} people`);
      }
      if (parsed.detectedOccasion) {
        state.occasion = parsed.detectedOccasion;
        if (el.occasionInput) el.occasionInput.value = state.occasion;
        renderCategory();
        msgs.push(`Occasion: ${state.occasion}`);
      }

      if (el.billScanBanner && el.billScanMessage) {
        el.billScanMessage.textContent = msgs.length > 0
          ? `✓ Scanned from "${filename}": ${msgs.join(' · ')}`
          : `✓ Receipt attached from "${filename}". Please verify amount.`;
        el.billScanBanner.style.display = 'flex';
        setTimeout(() => {
          if (el.billScanBanner) el.billScanBanner.style.display = 'none';
        }, 6000);
      }

      saveActiveState();
      calculateSplit();
    }

    if (el.btnAttachQr && el.qrFileInput) {
      el.btnAttachQr.addEventListener('click', () => {
        el.qrFileInput.click();
      });

      el.qrFileInput.addEventListener('change', (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
          alert('Please upload an image file for your payment QR code.');
          return;
        }

        const reader = new FileReader();
        reader.onload = (ev) => {
          savePaymentQr(ev.target.result);
          showToast('✓ Real Payment QR saved & attached.');
          if (state.activeResult) {
            calculateSplit();
          }
        };
        reader.readAsDataURL(file);
      });
    }

    if (el.btnRemoveQr) {
      el.btnRemoveQr.addEventListener('click', () => {
        savePaymentQr(null);
        if (el.qrFileInput) el.qrFileInput.value = '';
        showToast('Payment QR removed.');
        if (state.activeResult) {
          calculateSplit();
        }
      });
    }

    if (el.currencySelect) {
      el.currencySelect.addEventListener('change', (e) => {
        saveCurrencyPreference(e.target.value);
        renderCurrency();
        showToast(`Default currency saved as ${state.currencyCode}`);
      });
    }

    if (el.taxButtons) {
      el.taxButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
          el.taxButtons.forEach(b => b.classList.remove('active'));
          e.target.classList.add('active');
          state.taxPercent = parseInt(e.target.getAttribute('data-tax'), 10) || 0;
          saveActiveState();
          calculateSplit();
        });
      });
    }

    el.tipButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
        el.tipButtons.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        state.tipPercent = parseInt(e.target.getAttribute('data-tip'), 10) || 0;
        saveActiveState();
        calculateSplit();
      });
    });

    if (el.btnCalculate) {
      el.btnCalculate.addEventListener('click', () => {
        calculateSplit();
      });
    }

    if (el.btnSaveHistory) {
      el.btnSaveHistory.addEventListener('click', () => {
        saveCurrentBillToHistory();
      });
    }

    if (el.btnShareReport) {
      el.btnShareReport.addEventListener('click', () => {
        openReportModalWithItem(state.activeResult);
      });
    }

    if (el.btnPrintReceipt) {
      el.btnPrintReceipt.addEventListener('click', () => {
        openReportModalWithItem(state.activeResult);
        setTimeout(() => window.print(), 200);
      });
    }

    if (el.tabCalculator) {
      el.tabCalculator.addEventListener('click', () => switchTab('calculator'));
    }
    if (el.tabHistory) {
      el.tabHistory.addEventListener('click', () => switchTab('history'));
    }

    if (el.historySearchInput) {
      el.historySearchInput.addEventListener('input', () => {
        updateHistoryUI();
      });
    }

    if (el.btnClearHistory) {
      el.btnClearHistory.addEventListener('click', () => {
        if (state.history.length === 0) return;
        if (confirm('Clear all saved bills from history?')) {
          state.history = [];
          saveHistoryToStorage();
          showToast('History cleared.');
        }
      });
    }

    if (el.btnCloseReportModal) {
      el.btnCloseReportModal.addEventListener('click', () => {
        if (el.reportModal) el.reportModal.style.display = 'none';
      });
    }

    if (el.reportModal) {
      el.reportModal.addEventListener('click', (e) => {
        if (e.target === el.reportModal) {
          el.reportModal.style.display = 'none';
        }
      });
    }
  }

  function syncQuickPeopleButtons(currentCount) {
    el.quickCountButtons.forEach(btn => {
      const c = parseInt(btn.getAttribute('data-count'), 10);
      btn.classList.toggle('active', c === currentCount);
    });
  }

  // Initialize
  function init() {
    initDOM();
    loadPersistedData();

    if (el.currencySelect) {
      el.currencySelect.innerHTML = '';
      CURRENCIES.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.code;
        opt.textContent = `${c.symbol} ${c.code} — ${c.name}`;
        el.currencySelect.appendChild(opt);
      });
    }

    if (el.occasionInput) el.occasionInput.value = state.occasion;
    if (el.payerInput) el.payerInput.value = state.payer;
    if (el.amountInput) el.amountInput.value = state.amount;
    if (el.peopleInput) el.peopleInput.value = state.peopleCount;

    if (el.taxButtons) {
      el.taxButtons.forEach(b => {
        const taxVal = parseInt(b.getAttribute('data-tax'), 10);
        b.classList.toggle('active', taxVal === state.taxPercent);
      });
    }

    el.tipButtons.forEach(b => {
      const tipVal = parseInt(b.getAttribute('data-tip'), 10);
      b.classList.toggle('active', tipVal === state.tipPercent);
    });

    syncQuickPeopleButtons(state.peopleCount);
    renderCategory();
    renderCurrency();
    renderPaymentQrUI();
    renderUploadedBillUI();
    renderParticipantNamesInputGrid();
    bindEvents();
    updateHistoryUI();

    if (state.activeResult) {
      renderResults();
    } else {
      calculateSplit();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
