FROM adesh0303/eks-app:py-base

LABEL app="DeleteuserService"

COPY deleteuser_service.py .
# Create non-root user
RUN useradd -m -u 1000 appuser
# Change ownership
RUN chown -R appuser:appuser /app
# Switch to non-root user
USER appuser

EXPOSE 5000

CMD ["python", "deleteuser_service.py"]

