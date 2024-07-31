const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

// Initialize express app
const app = express();
const port = 1245;

// Create a list of products
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Redis client setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to get an item by its ID
const getItemById = (id) => {
  return listProducts.find(product => product.id === id);
};

// Route to get all products
app.get('/list_products', (req, res) => {
  const response = listProducts.map(product => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock
  }));
  res.json(response);
});

// Route to get product details
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - (reservedStock || 0);

  res.json({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity
  });
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    return res.status(404).json({ status: 'Product not found' });
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.stock - (reservedStock || 0);

  if (currentQuantity <= 0) {
    return res.json({
      status: 'Not enough stock available',
      itemId: itemId
    });
  }

  await reserveStockById(itemId, (reservedStock || 0) + 1);
  res.json({
    status: 'Reservation confirmed',
    itemId: itemId
  });
});

// Reserve stock by ID
const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

// Get current reserved stock by ID
const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return parseInt(stock, 10) || 0;
};

// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
