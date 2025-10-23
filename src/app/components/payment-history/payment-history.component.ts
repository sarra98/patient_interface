import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PaymentService, Payment, PaymentReceipt } from '../../services/payment.service';

@Component({
  selector: 'app-payment-history',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './payment-history.component.html',
  styleUrls: ['./payment-history.component.css']
})
export class PaymentHistoryComponent implements OnInit {
  payments: Payment[] = [];
  filteredPayments: Payment[] = [];
  
  isLoading = true;
  error = '';
  successMessage = '';
  
  // Filtres
  currentFilter = 'all';
  searchTerm = '';
  
  // Modal de reçu
  showReceiptModal = false;
  currentReceipt: PaymentReceipt | null = null;
  isLoadingReceipt = false;

  constructor(private paymentService: PaymentService) {}

  ngOnInit() {
    this.loadPayments();
  }

  loadPayments() {
    this.isLoading = true;
    this.paymentService.getPayments().subscribe({
      next: (response) => {
        this.payments = response.paiements.sort((a, b) => 
          new Date(b.date_paiement).getTime() - new Date(a.date_paiement).getTime()
        );
        this.applyFilters();
        this.isLoading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement de l\'historique des paiements';
        this.isLoading = false;
        console.error('Error loading payments:', error);
      }
    });
  }

  applyFilters() {
    let filtered = [...this.payments];
    
    // Filtre par statut
    if (this.currentFilter !== 'all') {
      filtered = filtered.filter(payment => payment.statut === this.currentFilter);
    }
    
    // Filtre par recherche
    if (this.searchTerm.trim()) {
      const term = this.searchTerm.toLowerCase();
      filtered = filtered.filter(payment => 
        payment.reference_transaction?.toLowerCase().includes(term) ||
        payment.rendez_vous?.motif?.toLowerCase().includes(term) ||
        payment.rendez_vous?.medecin?.nom?.toLowerCase().includes(term) ||
        payment.rendez_vous?.medecin?.prenom?.toLowerCase().includes(term)
      );
    }
    
    this.filteredPayments = filtered;
  }

  onFilterChange(filter: string) {
    this.currentFilter = filter;
    this.applyFilters();
  }

  onSearchChange() {
    this.applyFilters();
  }

  viewReceipt(payment: Payment) {
    if (payment.statut !== 'valide') {
      this.error = 'Le reçu n\'est disponible que pour les paiements validés';
      setTimeout(() => this.error = '', 3000);
      return;
    }

    this.isLoadingReceipt = true;
    this.showReceiptModal = true;

    this.paymentService.getPaymentReceipt(payment.id).subscribe({
      next: (response) => {
        this.currentReceipt = response.recu;
        this.isLoadingReceipt = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement du reçu';
        this.closeReceiptModal();
        this.isLoadingReceipt = false;
        setTimeout(() => this.error = '', 3000);
      }
    });
  }

  closeReceiptModal() {
    this.showReceiptModal = false;
    this.currentReceipt = null;
  }

  printReceipt() {
    if (this.currentReceipt) {
      window.print();
    }
  }

  downloadReceipt() {
    if (!this.currentReceipt) return;

    const receiptContent = this.generateReceiptHTML(this.currentReceipt);
    const blob = new Blob([receiptContent], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `recu_${this.currentReceipt.numero_recu}.html`;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  private generateReceiptHTML(receipt: PaymentReceipt): string {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Reçu de paiement - ${receipt.numero_recu}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 20px; }
          .header { text-align: center; margin-bottom: 30px; }
          .info { margin: 10px 0; }
          .amount { font-size: 1.2em; font-weight: bold; color: #28a745; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>Reçu de paiement</h1>
          <p>N° ${receipt.numero_recu}</p>
        </div>
        
        <div class="info"><strong>Date d'émission :</strong> ${this.formatDate(receipt.date_emission)}</div>
        <div class="info"><strong>Patient :</strong> ${receipt.patient.prenom} ${receipt.patient.nom}</div>
        <div class="info"><strong>Email :</strong> ${receipt.patient.email}</div>
        
        <hr>
        
        <div class="info"><strong>Consultation du :</strong> ${receipt.rendez_vous ? this.formatDate(receipt.rendez_vous.date) : 'N/A'}</div>
        <div class="info"><strong>Médecin :</strong> ${receipt.rendez_vous?.medecin || 'N/A'}</div>
        <div class="info"><strong>Motif :</strong> ${receipt.rendez_vous?.motif || 'N/A'}</div>
        
        <hr>
        
        <div class="info"><strong>Mode de paiement :</strong> ${this.getPaymentTypeLabel(receipt.paiement.type_paiement)}</div>
        <div class="info"><strong>Référence :</strong> ${receipt.paiement.reference_transaction}</div>
        <div class="info amount"><strong>Montant payé :</strong> ${this.formatAmount(receipt.paiement.montant)}</div>
        
        <hr>
        
        <p><em>Ce reçu fait foi de paiement.</em></p>
      </body>
      </html>
    `;
  }

  formatAmount(amount: number): string {
    return this.paymentService.formatAmount(amount);
  }

  formatDate(dateString: string): string {
    return this.paymentService.formatDate(dateString);
  }

  getPaymentStatusLabel(status: string): string {
    return this.paymentService.getPaymentStatusLabel(status);
  }

  getPaymentStatusClass(status: string): string {
    return this.paymentService.getPaymentStatusClass(status);
  }

  getPaymentTypeLabel(type: string): string {
    return this.paymentService.getPaymentTypeLabel(type);
  }

  getPaymentTypeIcon(type: string): string {
    return this.paymentService.getPaymentTypeIcon(type);
  }

  get paymentCounts() {
    return {
      all: this.payments.length,
      valide: this.payments.filter(p => p.statut === 'valide').length,
      en_attente: this.payments.filter(p => p.statut === 'en_attente').length,
      echec: this.payments.filter(p => p.statut === 'echec').length,
      rembourse: this.payments.filter(p => p.statut === 'rembourse').length
    };
  }

  get totalAmount() {
    return this.payments
      .filter(p => p.statut === 'valide')
      .reduce((total, p) => total + p.montant, 0);
  }
}
