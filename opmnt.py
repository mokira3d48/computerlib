# -*- encoding : utf-8 -*

# author  : Dr Mokira
# created : 2020-08-02
# updated : 2020-08-02


from mnt 	import Monitor
from op 	import Operating


"""
"""


class OperatingMonitor( Monitor ) :

	def __init__( self ) :
		super( OperatingMonitor, self ).__init__();


	# Overide
	def connect( self, _obj_ ) :
		if isinstance( _obj_,  Operating ) :
			super().connect( _obj_ );
			self.addField( 'progress purcent', 'progressv' );
			self.addField( 'task length',      'weight' );


	# Overide
	def valueOf( self, attrname ) :
		p = super().valueOf( attrname );


		if attrname == 'progressv' :
			return p * 100 / self._object.weight;

		return p;

	# Overide
	def format( self, attrname, value ) :
		vstr = super().format( attrname, value );

		if attrname == 'progressv' :
			return "{} %".format( vstr );

		return vstr;




#end




if __name__ == '__main__' :

	import time

	class printing( Operating ) :

		def __init__( self ) :
			super( printing, self ).__init__();


		# Overide
		def run( self ) :
			n = self.argv[0];
			self.increaseWeight( n );

			for i in range( n ) :
				self.progress( 1 );
#				print( f"Printing i : {i}" );
				time.sleep( 1 );

	#end

	p  = printing();
	mp = OperatingMonitor();

	mp.connect( p );


	p( 15 ).start();
	print( "Lauch ..." );
	mp.monitoring.start();

#	time.sleep( 5 );
	p.waitEnd();
	mp.monitoring.stop();
	print( "Terminated." );































#end