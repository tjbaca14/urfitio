const apiClient = axios.default.create({
  baseURL: "/",
  withCredentials: true,
  headers: {
    Accept: "application/json", // Add this header to identify API requests
  },
});

apiClient.interceptors.request.use(
  (config) => {
    console.log("Request made with:", config);
    return config;
  },
  (error) => {
    console.error("Request error:", error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      const excludedRoutes = ["/api/v1/token"]; // Add any other routes you want to exclude
    // Check if the request URL matches an excluded route
      const requestUrl = error.config?.url || "";
      const isExcluded = excludedRoutes.some((route) => requestUrl.includes(route));
      if (!isExcluded && error.response?.status === 401) {
        // Handle 401 errors for non-excluded routes
        console.warn("Session expired. Redirecting to login.");
        window.location.href = "/login";
      }
  
    }
    return Promise.reject(error);
  }
);

// Export the Axios instance
export { apiClient };
