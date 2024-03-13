import Melody
import ProgressionAccords
import Rythme
import mingus.core.intervals as intervals
import ContrePoint

'''
rythme = Rythme.Rythme((0,0))
rythme.generer_rythme()
progression = ProgressionAccords.ProgressionAccords(8,"D")
progression.genererProgressionAccords()
'''
melody = Melody.Melody(8, "D", (3, 4))
melody.generer_melodie()
print("tritone", intervals.measure("C", "F#"))

contrepoint = ContrePoint.ContrePoint(8, "C")
contrepoint.verifier_melodie()
