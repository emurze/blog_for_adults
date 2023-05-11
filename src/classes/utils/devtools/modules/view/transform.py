class Transform:
    @staticmethod
    def get_memory(bits_amount: int, /) -> str:
        """Transform bits to bytes and bytes to KB, MB, GB"""
        bit_to_byte_ratio = 8
        bits_amount //= bit_to_byte_ratio
        ext = 'B'
        extensions = ["KB", "MB", "GB", "TB"]
        while bits_amount > 1000 and len(extensions) > 0:
            ext = extensions.pop(0)
            bits_amount //= 1000
        return f"{bits_amount:.0f} {ext}"

    @staticmethod
    def get_time(time: float, /) -> str:
        """Transform time format in s and ms"""
        ext = 's'
        if time < 0.001:
            ext = 'ms'
            time *= 1000
        return f"{time:.3f}{ext}"
