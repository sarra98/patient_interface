import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PaymentRequest {
  rendez_vous_id: number;
  montant: number;
  type_paiement: 'carte_bancaire' | 'carte_postale';
  
  // Données carte bancaire
  numero_carte?: string;
  nom_porteur?: string;
  date_expiration?: string;
  cvv?: string;
  
  // Données carte postale
  numero_ccp?: string;
  cle_ccp?: string;
}

export interface Payment {
  id: number;
  rendez_vous_id: number;
  patient_id: number;
  montant: number;
  type_paiement: string;
  statut: string;
  reference_transaction: string;
  date_paiement: string;
  rendez_vous?: {
    id: number;
    date_rdv: string;
    motif: string;
    medecin?: {
      nom: string;
      prenom: string;
      specialite: string;
    };
  };
}

export interface PaymentReceipt {
  numero_recu: string;
  date_emission: string;
  paiement: Payment;
  patient: {
    nom: string;
    prenom: string;
    email: string;
  };
  rendez_vous?: {
    date: string;
    motif: string;
    medecin: string;
  };
}

export interface Tarif {
  prix: number;
  description: string;
}

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private apiUrl = '/api/payments';

  constructor(private http: HttpClient) {}

  private getHeaders(): { headers: HttpHeaders } {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      })
    };
  }

  processPayment(paymentData: PaymentRequest): Observable<{ message: string; success: boolean; paiement?: Payment }> {
    return this.http.post<{ message: string; success: boolean; paiement?: Payment }>(
      this.apiUrl,
      paymentData,
      this.getHeaders()
    );
  }

  getPayments(): Observable<{ paiements: Payment[] }> {
    return this.http.get<{ paiements: Payment[] }>(
      this.apiUrl,
      this.getHeaders()
    );
  }

  getPaymentReceipt(paymentId: number): Observable<{ recu: PaymentReceipt }> {
    return this.http.get<{ recu: PaymentReceipt }>(
      `${this.apiUrl}/${paymentId}/receipt`,
      this.getHeaders()
    );
  }

  getTarifs(): Observable<{ tarifs: { [key: string]: Tarif } }> {
    return this.http.get<{ tarifs: { [key: string]: Tarif } }>(
      `${this.apiUrl}/tarifs`,
      this.getHeaders()
    );
  }

  getAppointmentTarif(appointmentId: number): Observable<{ tarif: number; type_consultation: string; rendez_vous: any }> {
    return this.http.get<{ tarif: number; type_consultation: string; rendez_vous: any }>(
      `${this.apiUrl}/rendez-vous/${appointmentId}/tarif`,
      this.getHeaders()
    );
  }

  // Utilitaires pour les cartes
  formatCardNumber(cardNumber: string): string {
    return cardNumber.replace(/\s/g, '').replace(/(.{4})/g, '$1 ').trim();
  }

  validateCardNumber(cardNumber: string): boolean {
    const cleaned = cardNumber.replace(/\s/g, '');
    return /^\d{16,19}$/.test(cleaned);
  }

  validateExpiryDate(expiryDate: string): boolean {
    if (!/^\d{2}\/\d{2}$/.test(expiryDate)) {
      return false;
    }

    const [month, year] = expiryDate.split('/').map(num => parseInt(num, 10));
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear() % 100;
    const currentMonth = currentDate.getMonth() + 1;

    if (month < 1 || month > 12) {
      return false;
    }

    if (year < currentYear || (year === currentYear && month < currentMonth)) {
      return false;
    }

    return true;
  }

  validateCVV(cvv: string): boolean {
    return /^\d{3,4}$/.test(cvv);
  }

  validateCCP(numeroCCP: string): boolean {
    const cleaned = numeroCCP.replace(/\s/g, '');
    return /^\d{10,20}$/.test(cleaned);
  }

  validateCCPKey(cle: string): boolean {
    return /^\d{2}$/.test(cle);
  }

  getCardType(cardNumber: string): string {
    const cleaned = cardNumber.replace(/\s/g, '');
    
    if (/^4/.test(cleaned)) {
      return 'visa';
    } else if (/^5[1-5]/.test(cleaned)) {
      return 'mastercard';
    } else if (/^3[47]/.test(cleaned)) {
      return 'amex';
    }
    
    return 'unknown';
  }

  getPaymentStatusLabel(status: string): string {
    const labels: { [key: string]: string } = {
      'en_attente': 'En attente',
      'valide': 'Validé',
      'echec': 'Échec',
      'rembourse': 'Remboursé'
    };
    return labels[status] || status;
  }

  getPaymentStatusClass(status: string): string {
    const classes: { [key: string]: string } = {
      'en_attente': 'warning',
      'valide': 'success',
      'echec': 'danger',
      'rembourse': 'info'
    };
    return classes[status] || 'secondary';
  }

  getPaymentTypeLabel(type: string): string {
    const labels: { [key: string]: string } = {
      'carte_bancaire': 'Carte bancaire',
      'carte_postale': 'Carte postale (CCP)',
      'especes': 'Espèces'
    };
    return labels[type] || type;
  }

  getPaymentTypeIcon(type: string): string {
    const icons: { [key: string]: string } = {
      'carte_bancaire': 'fas fa-credit-card',
      'carte_postale': 'fas fa-money-check',
      'especes': 'fas fa-coins'
    };
    return icons[type] || 'fas fa-money-bill';
  }

  formatAmount(amount: number): string {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR'
    }).format(amount);
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }
}
