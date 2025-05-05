<template>
  <v-container class="invoice-detail-page"
               fluid
  >
    <v-card class="pa-6 mt-4"
            color="primary"
            :loading="loading"
            :disabled="loading"
    >
      <v-card-title>
        <v-icon left>
          mdi-file-document-outline
        </v-icon>
        Invoice #{{ invoice.id }}
      </v-card-title>
      <v-divider />

      <v-row class="mt-4">
        <v-col cols="6">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Client Name</v-list-item-title>
              <v-list-item-subtitle>{{ invoice.clientName }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Client Address</v-list-item-title>
              <v-list-item-subtitle>{{ invoice.clientAddress }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>

        <v-col cols="6">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Invoice Date</v-list-item-title>
              <v-list-item-subtitle>{{ invoice.date }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Due Date</v-list-item-title>
              <v-list-item-subtitle>{{ invoice.dueDate }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-col>
      </v-row>

      <v-divider class="my-4" />

      <v-table class="mt-4 text-center">
        <thead>
          <tr class="">
            <th class="">
              Description
            </th>
            <th class="text-right">
              Quantity
            </th>
            <th class="text-right">
              Unit Price
            </th>
            <th class="text-right">
              Total Price
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in invoice.items">
            <td class="text-left">
              {{ item.description }}
            </td>
            <td class="text-right">
              {{ item.quantity }}
            </td>
            <td class="text-right">
              {{ formatPrice(item.unitPrice) }}
            </td>
            <td class="text-right">
              {{ formatPrice(item.totalPrice) }}
            </td>
          </tr>
        </tbody>
      </v-table>
      <!-- Payment Description -->
      <v-divider class="my-4" />
      <v-row class="mt-4">
        <v-col cols="6">
          <v-card-text>
            Please make sure to pay the amount by the due date to avoid late fees.
            For any inquiries, contact our support team at support@example.com.
          </v-card-text>
        </v-col>
        <v-col cols="6">
          <v-row>
            <v-col cols="12"
                   class="text-right"
            >
              <v-subheader>Total: {{ formatPrice(invoice.total) }}</v-subheader>
            </v-col>
            <v-col cols="12"
                   class="text-right"
            >
              <v-btn size="large"
                     color="green"
                     variant="flat"
                     @click="go"
              >
                Pay Now
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import { useUtilsStore } from '~/store/utils'

const route = useRoute()
const invoice = ref({
  id: 32,
  clientName: 'John Doe',
  clientAddress: '123 Business St, Suite 100',
  date: '2024-11-11',
  dueDate: '2024-11-25',
  items: [
    { description: 'Service A', quantity: 2, unitPrice: 2.5, totalPrice: 2.5 },
    { description: 'Service B', quantity: 1, unitPrice: 1.5, totalPrice: 1.5 },
    { description: 'Service C', quantity: 1, unitPrice: 1, totalPrice: 1 },
  ],
  total: 5,
})

function formatPrice(price) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(price)
}
const { t } = useI18n()
const utilStore = useUtilsStore()
const { stripe } = useClientStripe()

const loading = ref(false)

const go = async () => {
  loading.value = true
  const { data, error } = await useAuthAPIFetch('/api/v1/payment/create-checkout-session/', {
    method: 'POST',
  })
  if (error.value) {
    utilStore.showErrorMessage(error.value)
    loading.value = false
  }
  else {
    if (data.value.error) {
      utilStore.showErrorMessage(data.value.error)
    }
    else {
      utilStore.showSuccessMessage('redirecting')
      stripe.value.redirectToCheckout({ sessionId: data.value.session_id })
    }
  }
}
</script>

<style scoped>
.invoice-detail-page {
    max-width: 800px;
    margin: auto;
}
</style>
