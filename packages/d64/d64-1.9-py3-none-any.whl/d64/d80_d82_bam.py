from .bam import BAM


class D80D82BAM(BAM):

    BAM_OFFSET = 6
    BAM_ENTRY_SIZE = 5

    def get_entry(self, track):
        """Return a tuple of total free blocks and a string of free blocks for a track."""
        if track < self.image.MIN_TRACK or track > self.image.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        for block in self.image.bam_blocks:
            first_track, end = block.track_range
            if track <= end:
                break
        start = self.BAM_OFFSET+(track-first_track)*self.BAM_ENTRY_SIZE
        e = tuple(block.get(start, start+self.BAM_ENTRY_SIZE))
        free_bits = ''
        for b in e[1:]:
            free_bits += ''.join(reversed(format(b, '08b')))

        return e[0], free_bits

    def set_entry(self, track, total, free_bits):
        """Update the block allocation entry for a track."""
        if track < self.image.MIN_TRACK or track > self.image.MAX_TRACK:
            raise ValueError("Invalid track, %d" % track)

        for block in self.image.bam_blocks:
            first_track, end = block.track_range
            if track < end:
                break
        start = self.BAM_OFFSET+(track-first_track)*self.BAM_ENTRY_SIZE
        entry = [total]
        while free_bits:
            val = ''.join(reversed(free_bits[:8]))
            entry.append(int(val, 2))
            free_bits = free_bits[8:]
        bin_entry = bytes(entry)
        block.set(start, bin_entry)
