# Use Node 20 LTS image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

# Expose port used by Vite
EXPOSE 5173

# Default command
CMD ["npm", "run", "dev","--", "--host"]
