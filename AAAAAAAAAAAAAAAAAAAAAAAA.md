    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("🔌 Desconectado do MongoDB")
