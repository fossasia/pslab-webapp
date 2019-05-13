print_('Voltages')

for a in ['CH1','CH2','CH3','AN8','CAP','SEN']:
	button('Voltage : %s'%a,"get_voltage('%s')"%a,"display_number")
	print('') #Just to get a newline

print('')
print_('Passive Elements')
button('Capacitance_:',"get_capacitance()","display_number")
print('')
button('Resistance__:',"get_resistance()","display_number")
