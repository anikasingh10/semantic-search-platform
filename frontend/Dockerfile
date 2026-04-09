# Build stage
FROM node:18 AS builder
WORKDIR /app

# Install dependencies first (for caching)
COPY package*.json ./
RUN npm install

# Copy rest of code
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app

# Copy only necessary files
COPY --from=builder /app ./

EXPOSE 3000

CMD ["npm", "start"]