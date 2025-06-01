# import for django_rest_framework tests
from rest_framework.test import APITestCase

from .models import Expense
"""
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateField(auto_now_add=True)
    #category choice field
    CATEGORY_CHOICES = (
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )

    def __str__(self):
        return f"{self.name} - {self.amount}"
"""
class ExpenseAPITestCase(APITestCase):
    def setUp(self):
        # Create 3 expenses
        Expense.objects.bulk_create([
            Expense(name='Food', amount=100.00, category='Food'),
            Expense(name='Transport', amount=50.00, category='Transport'),
            Expense(name='Utility', amount=75.00, category='Utility')            
        ])

    def test_expenses_list(self):     
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        
    def test_expense_detail(self):
        response = self.client.get('/api/expenses/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Food')
        self.assertEqual(float(response.json()['amount']), 100.00)
        self.assertEqual(response.json()['category'], 'Food')   
    
    def test_expense_create(self):  
        response = self.client.post('/api/expenses/', {
            'name': 'Food',
            'amount': '10.00',
            'category': 'food',
        })  
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Food')
        self.assertEqual(response.json()['amount'], '10.00')
        self.assertEqual(response.json()['category'], 'food')

    def test_expense_update(self):
        response = self.client.put('/api/expenses/1/', {
            'name': 'Pizaa',
            'amount': '15.00',
            'category': 'food'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Pizaa')
        self.assertEqual(response.json()['amount'], '15.00')
        self.assertEqual(response.json()['category'], 'food')

    def test_expense_delete(self):
        response = self.client.delete('/api/expenses/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Expense.objects.all()), 2)
        self.assertRaises(Expense.DoesNotExist, Expense.objects.get, pk=1)  
        response = self.client.get('/api/expenses/2/')  
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        # Clean up the created expenses
        Expense.objects.all().delete()
   
